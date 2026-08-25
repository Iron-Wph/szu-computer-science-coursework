import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda, RunnableBranch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import re
from typing import List, Dict, Optional, Any
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
import requests
from pydantic import Field, BaseModel

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

class CustomServerChatModelConfig(BaseModel):
    """自定义服务器模型配置"""
    api_url: str = Field(..., description="API服务器地址")
    temperature: float = Field(default=0.3, description="温度参数")
    max_new_tokens: int = Field(default=1000, description="最大生成token数")

class CustomServerChatModel(BaseChatModel):
    """自定义服务器模型类"""
    config: CustomServerChatModelConfig
    def __init__(self, api_url: str, temperature: float = 0.3, max_new_tokens: int = 1000, **kwargs):
        config = CustomServerChatModelConfig(api_url=api_url, 
                                             temperature=temperature, max_new_tokens=max_new_tokens)
        super().__init__(config=config, **kwargs)
    def _clean_response_text(self, text: str) -> str:
        """
        清理模型回答中的标签和无用内容
        :param text: 模型原始回答文本
        :return: 清理后的文本
        """
        # 移除以#开头的标签内容（如 #中医药 #中草药知识）
        cleaned_text = re.sub(r'#\S+\s*', '', text)
        # 移除连续的多个标签行
        cleaned_text = re.sub(r'(^|\n)(\s*#[^\n]+\s*)+(\n|$)', '\n', cleaned_text)
        # 移除可能的标签列表（多行标签）
        tag_list_pattern = re.compile(r'(^|\n)(#[^\n]+\n){2,}', re.MULTILINE)
        cleaned_text = tag_list_pattern.sub('\n', cleaned_text)
        # 移除多余的空行
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
        # 移除开头和结尾的空白
        cleaned_text = cleaned_text.strip()
        return cleaned_text
    def _compress_chat_history(self, chat_history: str) -> str:
        """
        压缩聊天历史记录
        :param chat_history: 原始聊天历史记录
        :return: 压缩后的聊天历史记录
        """
        # 如果聊天历史为空，直接返回
        if not chat_history:
            return ""
            
        # 构建压缩聊天历史的提示词
        compress_prompt = f"""请将以下聊天历史压缩为简短的摘要，保留关键信息和上下文，但减少总体长度。
                聊天历史：
                {chat_history}
                请提供压缩后的摘要："""

        try:
            # 创建请求体
            request_data = {
                "prompt": compress_prompt,
                "max_new_tokens": 1000  # 限制摘要长度
            }
            
            # 调用API (使用POST请求)
            response = requests.post(
                f"{self.config.api_url}/generate", 
                json=request_data
            )
            response.raise_for_status()
            
            # 获取生成的文本
            compressed_history = response.json()["generated_text"]
            print(f"成功压缩聊天历史，原始长度: {len(chat_history)}，压缩后长度: {len(compressed_history)}")
            
            return compressed_history
        except Exception as e:
            print(f"压缩聊天历史时出错: {str(e)}")
            # 如果压缩失败，返回原始历史记录
            return chat_history
    def _generate(self, messages: List[Any], stop: Optional[List[str]] = None,
                   run_manager: Optional[Any] = None, **kwargs) -> ChatResult:
        """生成回答"""
        # 将消息列表转换为单个提示文本
        prompt = self._convert_messages_to_prompt(messages)        
        try:
            # 创建请求体
            request_data = {
                "prompt": prompt,
                "max_new_tokens": self.config.max_new_tokens
            }            
            # 调用API (使用POST请求)
            response = requests.post(
                f"{self.config.api_url}/generate", 
                json=request_data
            )
            response.raise_for_status()            
            # 获取生成的文本
            generated_text = response.json()["generated_text"]            
            # 清理生成的文本，移除标签和无用内容
            cleaned_text = self._clean_response_text(generated_text)            
            # 返回消息
            message = AIMessage(content=cleaned_text)
            return ChatResult(generations=[ChatGeneration(message=message)])
        except Exception as e:
            raise ValueError(f"调用API时出错: {str(e)}")

    def _convert_messages_to_prompt(self, messages: List[Any]) -> str:
        """将消息列表转换为提示文本"""
        prompt_parts = []
        for message in messages:
            if isinstance(message, SystemMessage):
                # 系统消息不添加标签
                prompt_parts.append(message.content)
            elif isinstance(message, HumanMessage):
                # 用户消息直接添加内容，不添加Human:标签
                prompt_parts.append(message.content)
            elif isinstance(message, AIMessage):
                # AI消息直接添加内容，不添加Assistant:标签
                prompt_parts.append(message.content)
        return "\n\n".join(prompt_parts)
    @property
    def _llm_type(self) -> str:
        return "custom_server_chat_model"

class RetrievalQA:
    def __init__(self, persist_directory: str = '../data_base/vector_db/chroma', 
                 temperature: float = 0.7, k: int = 3, 
                 server_url: str = "http://localhost:8000"):  # 添加服务器URL参数
        self.kb_manager = KnowledgeBaseManager(persist_directory=persist_directory)
        # 初始参数
        self.temperature = temperature
        self.k = k
        self.server_url = server_url  # 保存服务器URL
        # 提示词语模板类
        self.promptTemplates = PromptTemplates()
        self.chatLLM = self._initialize_llm()
        self.qa_history_chain = self._initialize_qa_chain()
        # 初始化会话历史记录管理
        self.session_histories = {}  # 使用字典存储不同会话的历史记录
        self.default_history_manager = ChatHistoryManager()  # 默认历史记录管理器，用于兼容旧代码

    def _initialize_llm(self):
        """
        初始化大语言模型。
        """
        return CustomServerChatModel(
            api_url=self.server_url,
            temperature=self.temperature,
            max_new_tokens=1000  # 设置默认的最大生成token数
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
        
        content_list = []
        for doc in documents:
            # 使用正则表达式移除所有以#开头的标签
            clean_content = re.sub(r'#\S+', '', doc.page_content).strip()
            if clean_content:
                content_list.append(clean_content)
            
        return "\n\n".join(content_list)

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
            query = self.promptTemplates.format_prompt(
                "rewrite_query",query=query)
        else:
            query = self.promptTemplates.format_prompt(
                "rewrite_query2",query=query,history=history)
        response = self.chatLLM.invoke(query)
        print(f"改写query: {response.content}")
        return response.content
    
    def extract_keywords(self,query:str) -> list[str]:
        """
        提取关键词
        :param query: 用户问题
        :return: 关键词列表
        """
        prompt = self.promptTemplates.format_prompt("keywords",text=query)
        response = self.chatLLM.invoke(prompt)
        print(f"提取关键词: {response.content}")
        return [kw.strip() for kw in response.content.split('<->') if kw.strip()]
    
    def generate_hyde_document(self, query: str, context_str: str) -> str:
        '''
        生成假设性的答案段落
        :param query: 用户问题
        :return: 假设性的答案段落
        '''
        prompt = self.promptTemplates.format_prompt(
            "hyde", context_str=context_str, query=query)
        response = self.chatLLM.invoke(prompt)
        print(f"生成假设性的答案: {response.content}")
        return response.content
    
    # 建立问答链
    def _initialize_qa_chain(self):
        """
        构建带有历史记录的问答链。
        """
        # 问答链的系统prompt
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", self.promptTemplates._get_system_prompt()),
            ("placeholder", "{chat_history}"),
            ("human", "{input}")
        ])
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
            print(f"初始的query: {query}")
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
            print(f"提取重写的query关键词{kw} 检索: {docs}")
        # 去重
        all_docs = self._deduplicate_docs(all_docs)
        # 排序
        for i, doc in enumerate(all_docs):
            print(f"所有doc分数: {i} {doc.metadata['source']} {doc.metadata['score']}")
        # 返回前k个文档
        return all_docs[:self.k]

    # 检索问答
    def invoke(self, question: str, session_id: str = None) -> dict:
        """
        调用问答链进行问答。
        :param question: 用户问题。
        :param session_id: 会话ID，用于区分不同的会话。
        :return: 包含answer和context的字典。
        """
        # 保存用户问题到聊天记录
        history_manager = self._get_history_manager(session_id)
        history_manager.add_message("user", question)
        # 获取聊天历史记录（原始格式，用于压缩）
        chat_history_raw = history_manager.get_formatted_history()
        # 检查是否包含URL
        url_match = is_url(question)
        if url_match:
            # 爬取网页内容
            url = url_match.group(0)
            print(f"检测到网页链接： {url}")
            md_path = crawl_website_to_markdown(url, max_pages=1) 
            with open(md_path, 'r', encoding='utf-8') as f:
                crawled_content = f.read()
            print(f"已爬取网页内容，长度: {len(crawled_content)} 字符")        
            # 构造Document对象并添加到知识库
            doc = Document(page_content=crawled_content, metadata={"source": url})
            self.kb_manager.add_documents([doc])            
            # 创建一个增强的问题，包含爬取的内容
            enhanced_question = f"""
#任务#
如果用户的问题范围很广，请根据网页内容中主要出现的知识点回答。
#网页内容#
{crawled_content}
#用户问题#
{question}
"""
            # 直接使用LLM回答，不进行多路检索
            system_prompt = self.promptTemplates._get_system_prompt()
            # print(f"系统提示词: {system_prompt}")
            # print(f"增强问题: {enhanced_question}")  # 只打印前100个字符            
            # 构建提示词
            combined_prompt = f"{system_prompt}\n{enhanced_question}"            
            # 直接使用单一字符串调用API
            try:
                request_data = {
                    "prompt": combined_prompt,
                    "max_new_tokens": self.chatLLM.config.max_new_tokens
                }                
                # 调用API (使用POST请求)
                response = requests.post(
                    f"{self.chatLLM.config.api_url}/generate", 
                    json=request_data
                )
                response.raise_for_status()                
                # 获取生成的文本
                answer = response.json()["generated_text"]                
                # 清理生成的文本
                answer = self.chatLLM._clean_response_text(answer)                
                # 清理回答开头的特殊字符，包括中文标点符号
                answer = re.sub(r'^[\s\?\!,，。、；：""''（）【】《》？！\n\r\t]+', '', answer)                
                print(f"成功获取回答，长度: {len(answer)}")
            except Exception as e:
                print(f"直接调用API时出错: {str(e)}")
                answer = f"抱歉，处理您的请求时出现错误: {str(e)}"
            # 添加 AI 回答到历史记录
            history_manager.add_message("assistant", answer)
            # 返回结果
            return {
                "answer": answer,
                "context": f"爬取的网页内容:\n{crawled_content}"
            }
        else:
            # 使用原有的多路检索流程
            result = self.qa_history_chain.invoke({
                "input": question,
                "chat_history": chat_history_raw  
            })
            # 清理回答开头的特殊字符
            if "answer" in result:
                result["answer"] = re.sub(r'^[\s\?\!,，。、；：""''（）【】\
                                          《》？！\n\r\t]+', '', result["answer"])
            # 添加 AI 回答到历史记录
            history_manager.add_message("assistant", result["answer"])            
            # 处理context，确保它是可序列化的
            context = result.get("context", [])
            if hasattr(context, '__iter__') and not isinstance(context, str):
                # 如果是Document对象列表，提取内容
                try:
                    context_texts = []
                    for doc in context:
                        if hasattr(doc, 'page_content'):
                            context_texts.append(doc.page_content)
                    context = '\n\n'.join(context_texts)
                except:
                    context = str(context)            
            # 返回可序列化的结果
            return {
                "answer": result.get("answer", "抱歉，我无法回答这个问题。"),
                "context": context
            }
        
    def _get_history_manager(self, session_id=None):
        """
        获取指定会话ID的历史记录管理器，如果不存在则创建新的。
        :param session_id: 会话ID
        :return: 对应的历史记录管理器
        """
        if session_id is None:
            return self.default_history_manager
            
        if session_id not in self.session_histories:
            self.session_histories[session_id] = ChatHistoryManager()
            
        return self.session_histories[session_id]

    # 历史聊天记录的管理
    def get_chat_history(self, session_id=None) -> List[Dict[str, str]]:
        """
        获取指定会话ID的聊天历史记录。
        :param session_id: 会话ID
        :return: 聊天历史记录列表
        """
        history_manager = self._get_history_manager(session_id)
        return history_manager.get_messages()

    def clear_chat_history(self, session_id=None):
        """
        清空指定会话ID的聊天历史记录。
        :param session_id: 会话ID，如果为None则清空所有会话记录
        """
        if session_id is None:
            # 清空所有会话记录
            self.session_histories = {}
            self.default_history_manager.clear_history()
        else:
            # 清空指定会话记录
            if session_id in self.session_histories:
                self.session_histories[session_id].clear_history()
            else:
                # 如果指定的会话ID不存在，创建一个新的空历史记录
                self.session_histories[session_id] = ChatHistoryManager()

    def get_formatted_history(self, session_id=None) -> str:
        """
        获取指定会话ID的格式化后的聊天历史（用于提示词注入）。
        :param session_id: 会话ID
        :return: 格式化后的历史字符串
        """
        history_manager = self._get_history_manager(session_id)
        return history_manager.get_formatted_history()
    
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
    res_with_history = qa_instance.invoke(question="你可以介绍一下他吗？", session_id="example_session")
    print(res_with_history) 