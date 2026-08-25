from typing import List
from langchain_core.embeddings import Embeddings
import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
class QWenEmbeddings(Embeddings):
    """`Zhipuai Embeddings` embedding models."""
    def __init__(self, batch_size: int = 10):
        """
        实例化ZhipuAI为values["client"]
        Args:
            values (Dict): 包含配置信息的字典，必须包含 client 的字段.
        Returns:
            values (Dict): 包含配置信息的字典。如果环境中有zhipuai库，则将返回实例化的ZhipuAI类；否则将报错 'ModuleNotFoundError: No module named 'zhipuai''.
        """
        from openai import OpenAI
        self.batch_size = batch_size  # 最大批次大小
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url=os.getenv("DASHSCOPE_API_BASE")  # 百炼服务的base_url
        )
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        生成输入文本列表的 embedding.
        Args:
            texts (List[str]): 要生成 embedding 的文本列表.
        Returns:
            List[List[float]]: 输入列表中每个文档的 embedding 列表。每个 embedding 都表示为一个浮点值列表。
        """
        if not texts:
            return []
        
        all_embeddings = []
        # 分批次处理文本
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i:i+self.batch_size]
            try:
                response = self.client.embeddings.create(
                    model=os.getenv("DASHSCOPE_EMBEDDING_MODEL"),
                    input=batch_texts,
                    dimensions=1024,
                    encoding_format="float"
                )
                batch_embeddings = [data.embedding for data in response.data]
                all_embeddings.extend(batch_embeddings)
            except openai.OpenAIError as e:
                raise RuntimeError(f"批次 {i//self.batch_size+1} 嵌入生成失败: {e}") from e
        return all_embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """
        生成输入文本的 embedding.
        Args:
            texts (str): 要生成 embedding 的文本.
        Return:
            embeddings (List[float]): 输入文本的 embedding，一个浮点数值列表.
        """

        return self.embed_documents([text])[0]


if __name__ == "__main__":
    from openai import OpenAI

    def qwen_embedding(text: str):
        client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
            base_url=os.getenv("DASHSCOPE_API_BASE")  # 百炼服务的base_url
        )

        completion = client.embeddings.create(
            model=os.getenv("DASHSCOPE_EMBEDDING_MODEL"),
            input=text,
            dimensions=1024, # 指定向量维度（仅 text-embedding-v3 支持该参数）
            encoding_format="float"
        )
        
        return completion