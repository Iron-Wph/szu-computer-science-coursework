import os
from typing import List, Dict, Union, Set
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from .qw_embedding import QWenEmbeddings
from .tool import rerank_with_dashscope
from .document_processor import DocumentProcessor

class KnowledgeBaseManager:
    def __init__(
        self,
        persist_directory: str = "../data_base/vector_db/chroma",
        knowledge_base_dir: str = "../documents",
    ):
        """
        初始化知识库管理器。
        :param persist_directory: Chroma数据库的存储路径。
        :param knowledge_base_dir: 知识库文档目录。
        """

        self.knowledge_base_dir = knowledge_base_dir
        self.persist_directory = persist_directory
        self.collection_name = "know"
        self.embedding = QWenEmbeddings()
        # 初始化文档处理器，用于拆分文档
        self.doc_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
        self._initialize_vectorstore()
        
        print(f"知识库管理器已初始化。向量数据库路径: {os.path.abspath(self.persist_directory)}")
        
    def get_existing_sources(self) -> Set[str]:
        """
        获取知识库中所有已存在的 source 路径。
        :return: 包含所有 source 的集合。
        """
        try:
            results = self.vectorstore.get(include=["metadatas"])
            sources = set()

            if "metadatas" in results:
                for metadata in results["metadatas"]:
                    source = metadata.get("source")
                    if source:
                        sources.add(source)
            return sources
        except Exception as e:
            print(f"获取现有 source 失败: {e}")
            return set()
    
    def _initialize_vectorstore(self):
        """
        初始化或加载Chroma向量存储，并加载现有目录的文档，不会重复添加。
        """
        # 如果目录不存在，Chroma会自动创建
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding,
            collection_name=self.collection_name
            )
        
        # 获取现有 source 路径
        existing_sources = self.get_existing_sources()
        raw_documents = self.doc_processor.load_directory(
            self.knowledge_base_dir,existing_sources=existing_sources)
        self.add_documents(raw_documents)

    def add_documents(self, documents: List[Document]):
        """
        向知识库中添加文档。
        :param documents: 待添加的LangChain Document对象列表。
        """
        if not documents:
            print("没有提供文档，跳过添加操作。")
            return
        print(f"拆分前文档数量: {len(documents)}")

        # 将文档拆分成更小的块
        documents = self.doc_processor.split_documents(documents)
        print(f"拆分后文档数量: {len(documents)}")

        self.vectorstore.add_documents(documents)
        self.vectorstore.persist()
        print(f"文档添加完成。当前知识库中共有 {self.vectorstore._collection.count()} 个文档块。")

    def query_documents(self, query: str, k: int = 3, rerank: bool = True) -> List[Document]:
        """
        从知识库中查询相关文档。
        :param query: 查询字符串。
        :param k: 返回最相关的文档数量。
        :param rerank: 选择是否需要重排序，默认使用。
        :return: 检索到的LangChain Document对象列表。
        """
        print(f"正在查询知识库，查询: '{query}'，返回 {k} 个结果...")
        # 默认是MMR + Rerank
        results = self.vectorstore.max_marginal_relevance_search(query, k=k)
        if rerank:
            # 使用DashScope API进行重排序
            scores = rerank_with_dashscope(query, results)
            # 根据重排序分数对文档进行排序
            results = [doc for _, doc in sorted(zip(scores, results), key=lambda x: x[0], reverse=True)]
            # 为重排序后的文档添加分数
            for doc, score in zip(results, scores):
                doc.metadata["score"] = score
            # 获取最终结果（取前k个）
            results = results[:k]
            print(f"使用了重排序模型")

        print(f"查询完成，检索到 {len(results)} 个文档块。")
        return results

    def delete_documents(self, ids: List[str] = None, where: Dict[str, Union[str, int, float, bool]] = None):
        """
        从知识库中删除文档。可以根据ID或元数据条件删除。
        :param ids: 待删除文档的ID列表（Chroma内部ID）。
        :param where: 基于文档元数据的过滤条件，例如 {"source": "my_document.pdf"}。
        """
        if not ids and not where:
            print("请提供要删除的文档ID或元数据条件。")
            return

        initial_count = self.vectorstore._collection.count()
        print(f"删除前知识库中共有 {initial_count} 个文档块。")

        if ids:
            print(f"正在删除指定ID的文档: {ids}...")
            self.vectorstore._collection.delete(ids=ids)
        elif where:
            print(f"正在删除符合条件的文档: {where}...")
            self.vectorstore._collection.delete(where=where)

        self.vectorstore.persist()
        final_count = self.vectorstore._collection.count()
        print(f"文档删除完成。当前知识库中共有 {final_count} 个文档块。共删除 {initial_count - final_count} 个文档块。")

    def delete_collection(self):
        """
        删除整个Chroma集合（即清空知识库）。
        """
        print("正在删除整个知识库集合...")
        try:
            self.vectorstore.delete_collection()
            # 删除持久化目录下的所有文件，确保彻底清除
            if os.path.exists(self.persist_directory):
                import shutil
                shutil.rmtree(self.persist_directory)
                print(f"已删除目录: {self.persist_directory}")
            self.vectorstore = self._initialize_vectorstore() # 重新初始化，确保对象可用
            print("知识库集合已成功删除并重新初始化。")
        except Exception as e:
            print(f"删除知识库集合失败: {str(e)}")

    def get_document_count(self) -> int:
        """获取知识库中存储的文档块数量（使用正确的集合）"""
        try:
            # 确保使用正确的集合
            collection = self.vectorstore._client.get_collection(
                name=self.collection_name
            )
            return collection.count()
        except Exception as e:
            print(f"获取文档数量失败: {e}")
            return 0
    
    def check_collection(self) -> None:
        """
        检查知识库中的文档
        """
        # 获取所有文档
        results = self.vectorstore.get(include=["documents", "metadatas"])

        # 打印文档内容和元数据
        for i, (doc, metadata) in enumerate(zip(results["documents"], results["metadatas"])):
            print(f"文档 {i + 1}:")
            print(f"  内容: {doc[:200]}...")  # 打印前200字符（防止内容过长）
            print(f"  元数据: {metadata}")

# 示例用法
if __name__ == "__main__":
    # 导入文档处理器，用于生成待添加的Document对象
    from document_processor import DocumentProcessor

    # 配置参数
    DOCUMENTS_DIR = "../documents"  # 替换为你的文档目录
    PERSIST_DIR = "../data_base/vector_db/chroma" # 测试用路径

    # 初始化文档处理器
    doc_processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)

    # 步骤1: 加载和处理文档
    print("\n--- 准备文档进行添加 ---")
    raw_documents = doc_processor.load_directory(DOCUMENTS_DIR)
    split_docs = doc_processor.split_documents(raw_documents)

    # 为测试，给文档添加一个独特的源标识，方便删除
    for i, doc in enumerate(split_docs):
        doc.metadata["id"] = f"doc_test_{i}"
        doc.metadata["source"] = "example_docs"

    # 初始化知识库管理器
    print("\n--- 初始化知识库管理器 ---")
    kb_manager = KnowledgeBaseManager(persist_directory=PERSIST_DIR)

    # 步骤2: 增加文档
    print("\n--- 增加文档到知识库 ---")
    kb_manager.add_documents(split_docs)
    print(f"当前知识库文档数量: {kb_manager.get_document_count()}")

    # 步骤3: 查询文档
    print("\n--- 查询知识库 ---")
    query_results = kb_manager.query_documents("什么是极限？", k=2, rerank=False)
    for i, doc in enumerate(query_results):
        print(f"\n查询结果 {i+1}:")
        print(f"  内容: {doc.page_content[:150]}...")
        print(f"  来源: {doc.metadata.get('source', 'N/A')}")
        print(f"  测试ID: {doc.metadata.get('test_id', 'N/A')}")

    # 步骤4: 删除指定文档（按元数据条件）
    print("\n--- 删除文档（按元数据条件）---")
    kb_manager.delete_documents(where={"test_source": "example_docs"})
    print(f"删除后知识库文档数量: {kb_manager.get_document_count()}")

    # 步骤5: 重新添加一些文档来测试删除ID
    print("\n--- 重新添加文档并测试按ID删除 ---")
    kb_manager.add_documents(split_docs[:2]) # 只添加前两个，方便获取ID
    print(f"重新添加后知识库文档数量: {kb_manager.get_document_count()}")

    # 获取前两个文档的ID
    # 注意：Chroma的文档ID是内部生成的，通常存储在metadata中，名为'id'
    # 这里的示例为了演示，假设前两个文档的ID可以从查询结果中获取
    ids_to_delete = [doc.metadata['id'] for doc in kb_manager.query_documents("", k=2,rerank=True)] # 查询所有文档获取ID
    print(f"准备删除的文档ID: {ids_to_delete}")
    kb_manager.delete_documents(ids=ids_to_delete)
    print(f"按ID删除后知识库文档数量: {kb_manager.get_document_count()}")

    # 步骤6: 删除整个知识库
    print("\n--- 删除整个知识库 ---")
    kb_manager.delete_collection()
    print(f"清空后知识库文档数量: {kb_manager.get_document_count()}")

    # 确认知识库是否真的清空了
    print("\n--- 再次确认知识库状态 ---")
    new_kb_manager = KnowledgeBaseManager(persist_directory=PERSIST_DIR) # 重新加载
    print(f"重新加载后知识库文档数量: {new_kb_manager.get_document_count()}")
