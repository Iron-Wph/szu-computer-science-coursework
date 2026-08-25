# import os
# from dotenv import load_dotenv, find_dotenv

# # 读取本地/项目的环境变量。
# # find_dotenv()寻找并定位.env文件的路径
# # load_dotenv()读取该.env文件，并将其中的环境变量加载到当前的运行环境中  
# # 如果你设置的是全局的环境变量，这行代码则没有任何作用。
# _ = load_dotenv(find_dotenv())

# # 如果你需要通过代理端口访问，你需要如下配置
# # os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
# # os.environ["HTTP_PROXY"] = 'http://127.0.0.1:7890'

# # 获取folder_path下所有文件路径，储存在file_paths里
# file_paths = []
# folder_path = '../../data_base/knowledge_db'
# for root, dirs, files in os.walk(folder_path):
#     for file in files:
#         file_path = os.path.join(root, file)
#         file_paths.append(file_path)
# print(file_paths[:3])


# print(completion.model_dump_json())

# from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader

# loader = UnstructuredMarkdownLoader("D:\\作业\\大三下\\大模型技术及应用\\期末大作业\\demo\\extracted_files_10d13b62-b59c-4db0-be92-fc4923374b6e\\full.md")
# md_pages = loader.load()
# print(f"载入后的变量类型为：{type(md_pages)}，",  f"该 Markdown 一共包含 {len(md_pages)} 页")
# md_page = md_pages[0]
# print(f"每一个元素的类型：{type(md_page)}.", 
#     f"该文档的描述性数据：{md_page.metadata}", 
#     f"查看该文档的内容:\n{md_page.page_content[0:][:200]}", 
#     sep="\n------\n")

# from langchain_community.document_loaders import PyMuPDFLoader

# # 创建一个 PyMuPDFLoader Class 实例，输入为待加载的 pdf 文档路径
# loader = PyMuPDFLoader("D:\\作业\\大三下\\大模型技术及应用\\期末大作业\\demo\\documents\\利用导数定义求解极限_杨德志.pdf")

# # 调用 PyMuPDFLoader Class 的函数 load 对 pdf 文件进行加载
# pdf_pages = loader.load()
# print(f"载入后的变量类型为：{type(pdf_pages)}，",  f"该 PDF 一共包含 {len(pdf_pages)} 页")
# pdf_page = pdf_pages[0]
# print(f"每一个元素的类型：{type(pdf_page)}.", 
#     f"该文档的描述性数据：{pdf_page.metadata}", 
#     f"查看该文档的内容:\n{pdf_page.page_content}", 
#     sep="\n------\n")


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader

# 自定义TextLoader以指定编码
class UTF8TextLoader(TextLoader):
    """TextLoader that uses UTF-8 encoding"""
    def __init__(self, file_path: str, encoding: str = "utf-8"):
        super().__init__(file_path, encoding=encoding)

# 使用自定义的UTF-8加载器
loader = DirectoryLoader(
    './documents',
    glob='**/*.md',
    loader_cls=UTF8TextLoader  # 关键修改：指定UTF-8编码
)
documents = loader.load()
# 打印加载的文档总数
print(f"成功加载 {len(documents)} 个文档")

# 查看每个文档的元数据和内容摘要
for i, doc in enumerate(documents):
    print(f"\n文档 {i+1}:")
    print(f"  元数据: {doc.metadata}")  # 通常包含文件名、路径等信息
    print(f"  内容长度: {len(doc.page_content)} 字符")
    print(f"  内容前100个字符: {doc.page_content}...")
    
    
    doc.page_content = doc.page_content.replace('\n\n', '\n')
    print(doc.page_content)

doc = documents[0]

############# 文档分割
#导入文本分割器
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 知识库中单段文本长度
CHUNK_SIZE = 500

# 知识库中相邻文本重合长度
OVERLAP_SIZE = 50
# 使用递归字符文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=OVERLAP_SIZE
)
# text_splitter.split_text(pdf_page.page_content[0:1000])
split_docs = text_splitter.split_documents([doc])
print(f"切分后的文件数量：{len(split_docs)}")
print(f"切分后的字符数（可以用来大致评估 token 数）：{sum([len(doc.page_content) for doc in split_docs])}")


## 嵌入向量
from utils.qw_embedding import QWenEmbeddings
import os
# 定义嵌入函数
embedding = QWenEmbeddings()
persist_directory = './data_base/vector_db/chroma'

# 打印绝对路径（确保路径正确）
abs_path = os.path.abspath(persist_directory)
print(f"向量数据库将保存到: {abs_path}")
from langchain_community.vectorstores import Chroma

vectordb = Chroma.from_documents(
    documents=split_docs,
    embedding=embedding,
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
)
print(f"向量库中存储的数量：{vectordb._collection.count()}")

question = "导数定义求极限的步骤是什么？"
# sim_docs = vectordb.similarity_search(question,k=3)
# print(f"检索到的内容数：{len(sim_docs)}")
# for i, sim_doc in enumerate(sim_docs):
#     print(f"检索到的第{i}个内容: \n{sim_doc.page_content[:200]}", end="\n--------------\n")

# 使用最大边际相关性检索
mmr_docs = vectordb.max_marginal_relevance_search(question,k=3)
for i, sim_doc in enumerate(mmr_docs):
    print(f"MMR 检索到的第{i}个内容: \n{sim_doc.page_content[:200]}", end="\n--------------\n")

from utils.tool import rerank_with_dashscope

# 步骤3: 使用DashScope API进行重排序
scores = rerank_with_dashscope(question, mmr_docs)

# 步骤4: 根据重排序分数对文档进行排序
sorted_results = [doc for _, doc in sorted(zip(scores, mmr_docs), key=lambda x: x[0], reverse=True)]

# 步骤5: 获取最终结果（取前k个）
k = 3
final_docs = sorted_results[:k]

# 打印结果
print(f"DashScope重排序后最终检索到的内容数：{len(final_docs)}")
for i, doc in enumerate(final_docs):
    print(f"排名第{i+1}的内容: \n{doc.page_content[:200]}", end="\n--------------\n")
    print(f"来源: {doc.metadata.get('source', '未知')}")
    print(f"相关性分数: {scores[mmr_docs.index(doc)]:.4f}")
