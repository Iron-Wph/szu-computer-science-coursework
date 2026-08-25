import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda, RunnableBranch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import re
from typing import List, Dict

# 从 utils/knowledgebase.py 导入 KnowledgeBaseManager
from .knowledgebase import KnowledgeBaseManager
# 从 utils/web_crawler.py 导入 crawl_website_to_markdown
from .web_crawler import crawl_website_to_markdown
# 导入提示词模板
from .prompts import PromptTemplates
# 导入历史记录管理模块
from .chat_history_manager import ChatHistoryManager
_ = load_dotenv(find_dotenv())  # read local .env file

def is_url(text):
    """
    检查文本是否包含有效的URL。
    """
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return url_pattern.search(text)

class RetrievalQA:
    def __init__(self, persist_directory: str = './data_base/vector_db/chroma', temperature: float = 0.3, k: int = 5):
        self.kb_manager = KnowledgeBaseManager(persist_directory=persist_directory)
        # 初始参数
        self.temperature = temperature
        self.k = k
        # 提示词语模板类
        self.promptTemplates = PromptTemplates()
        self.chatLLM = self._initialize_llm()
        self.qa_history_chain = self._initialize_qa_chain()
        # 初始化历史记录管理器
        self.history_manager = ChatHistoryManager()

    def _initialize_llm(self):
        """
        初始化大语言模型。
        """
        return ChatOpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url=os.getenv("DASHSCOPE_API_BASE"),
            model=os.getenv("DASHSCOPE_MODEL"),
            temperature=self.temperature
        )

    def _initialize_retriever(self):
        """
        初始化检索器。
        """
        return self.kb_manager.vectorstore.as_retriever(search_kwargs={"k": self.k})

    def _combine_docs(self, docs):
        """
        将多个文档对象（Document）的内容提取并连接成一个字符串。
        Args:
            docs: 文档列表或包含文档列表的字典
        Returns:
            str: 拼接后的文档内容
        """
        if isinstance(docs, dict) and "context" in docs:
            # 如果是字典格式且包含 context 键
            documents = docs["context"]
        elif isinstance(docs, list):
            # 如果直接是文档列表
            documents = docs
        else:
            # 如果是其他格式，返回空字符串
            return ""
            
        return "\n\n".join(doc.page_content for doc in documents)

    def _query_documents(self, query):
        return self.kb_manager.query_documents(query, k=self.k, rerank=True)

    def rewrite_query(self,query:str,history:list = None) -> str:
        """
        改写问题，根据是否有历史记录改写问题
        :param query: 用户问题
        :param history: 历史记录
        :return: 改写后的问题
        """
        if not history:
            return self.promptTemplates.format_prompt("rewrite_query",query=query)
        else:
            return self.promptTemplates.format_prompt("rewrite_query2",query=query,history=history)
    
    def extract_keywords(self,query:str) -> list[str]:
        """
        提取关键词
        :param query: 用户问题
        :return: 关键词列表
        """
        prompt = self.promptTemplates.format_prompt("keywords",text=query)
        response = self.chatLLM.invoke(prompt)
        return [kw.strip() for kw in response.content.split('<->') if kw.strip()]
    
    def generate_hyde_document(self, query: str, context_str: str) -> str:
        '''
        生成假设性的答案段落
        :param query: 用户问题
        :return: 假设性的答案段落
        '''
        prompt = self.promptTemplates.format_prompt("hyde", context_str=context_str, query=query)
        response = self.chatLLM.invoke(prompt)
        return response.content
    
    # 建立问答链
    def _initialize_qa_chain(self):
        """
        构建带有历史记录的问答链。
        """
        # # 构造 压缩问题的 prompt template
        # condense_question_prompt = ChatPromptTemplate([
        #     ("system", self.promptTemplates._get_condense_question_system_template()),
        #     ("placeholder", "{chat_history}"),
        #     ("human", "{input}"),
        # ])

        # # 构造检索文档的链
        # retrieve_docs = RunnableBranch(
        #     # 分支 1: 若聊天记录中没有 chat_history 则直接使用用户问题查询向量数据库
        #     (lambda x: not x.get("chat_history", False), (lambda x: x["input"]) | RunnableLambda(self._query_documents)),
        #     # 分支 2 : 若聊天记录中有 chat_history 则先让 llm 根据聊天记录完善问题再查询向量数据库
        #     condense_question_prompt | self.chatLLM | StrOutputParser() | self._initialize_retriever(),
        # )

        # 问答链的系统prompt
        # 制定prompt template
        qa_prompt = ChatPromptTemplate(
            [
                ("system", self.promptTemplates._get_system_prompt()),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        )

        # 定义问答链
        qa_chain = (
            RunnablePassthrough.assign(context=self._combine_docs)
            | qa_prompt
            | self.chatLLM
            | StrOutputParser()
        )

        # 使用多路检索
        def retrieve_docs(x):
            query = x["input"]
            history = x.get("chat_history", [])
            return self.multi_retrieval(query, history)
        
        # 定义带有历史记录的问答链
        qa_history_chain = RunnablePassthrough.assign(
            context = retrieve_docs
            ).assign(answer=qa_chain)

        return qa_history_chain

    def _deduplicate_docs(self, docs):
        """
        对文档列表进行去重，基于文档内容
        Args:
            docs: Document对象列表
        Returns:
            list: 去重后的Document对象列表
        """
        seen_contents = set()
        unique_docs = []
        for doc in docs:
            if doc.page_content not in seen_contents:
                seen_contents.add(doc.page_content)
                unique_docs.append(doc)
        return unique_docs
    
    # 多路检索
    def multi_retrieval(self, query: str, history: list = None) -> list[Document]:
        all_docs = []
        # 改写检索：根据是否有历史记录改写问题
        rewrite_query = self.rewrite_query(query, history)
        docs = self._query_documents(rewrite_query)
        all_docs.extend(docs)


        # 生成假设性的答案段落
        hyde_doc = self.generate_hyde_document(query, self._combine_docs(docs))
        hyde_docs = self._query_documents(hyde_doc)
        all_docs.extend(hyde_docs)

        # 提取重写的query关键词检索
        keywords = self.extract_keywords(rewrite_query)
        for kw in keywords:
            # 添加每个关键词检索到的文档
            docs = self._query_documents(kw)
            all_docs.extend(docs)

        # 去重
        all_docs = self._deduplicate_docs(all_docs)
        # 排序
        all_docs.sort(key=lambda x: x.metadata["score"], reverse=True)
        # 返回前k个文档
        return all_docs[:self.k]

    # 检索问答
    def invoke(self, question: str) -> str:
        """
        调用问答链进行问答。
        :param question: 用户问题。
        :return: 问答结果。
        """
        print(f"type(question):{type(question)}")
        # 保存用户问题到聊天记录
        self.history_manager.add_message("user", question)
        # 获取聊天历史记录
        chat_history = self.history_manager.get_formatted_history()

        # 检查是否包含URL
        if is_url(question):
            # 1. 爬取网页内容
            url = is_url(question).group(0)
            print(f"url 网页链接： {url}")

            md_path = crawl_website_to_markdown(url, max_pages=500)  # 可根据需要调整max_pages
            # 2. 读取markdown内容
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # 3. 构造Document对象
            doc = Document(page_content=content, metadata={"source": url})
            # 4. 临时加入知识库（可选：也可以直接用doc内容生成答案）
            self.kb_manager.add_documents([doc])
 
        # 返回检索内容
        result = self.qa_history_chain.invoke({
            "input": question,
            "chat_history": chat_history
        })
        # print(f"type(result):{type(result)}")
        # print(f"result:{result}")

        # 添加 AI 回答到历史记录
        self.history_manager.add_message("assistant", result["answer"])
        # 返回检索问答结果
        return result
        

    # 历史聊天记录的管理
    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        获取当前的聊天历史记录。
        :return: 聊天历史记录列表
        """
        return self.history_manager.get_messages()

    def clear_chat_history(self):
        """
        清空聊天历史记录。
        """
        self.history_manager.clear_history()

    def get_formatted_history(self) -> str:
        """
        获取格式化后的聊天历史（用于提示词注入）。
        :return: 格式化后的历史字符串
        """
        return self.history_manager.get_formatted_history()
    
if __name__ == "__main__":
    # 在这里添加测试代码
    qa_instance = RetrievalQA()

    # 测试无历史记录
    print("--- 测试无历史记录 ---")
    res_no_history = qa_instance.invoke(question="《利用导数定义求解极限》是谁写的？")
    print(res_no_history)

    # 测试带历史记录
    print("\n--- 测试带历史记录 ---")
    chat_history_example = [
        ("human", "《利用导数定义求解极限》是谁写的？"),
        ("ai", "利用导数定义求解极限》是杨德志写的。"),
    ]
    res_with_history = qa_instance.invoke(question="你可以介绍一下他吗？", chat_history=chat_history_example)
    print(res_with_history) 