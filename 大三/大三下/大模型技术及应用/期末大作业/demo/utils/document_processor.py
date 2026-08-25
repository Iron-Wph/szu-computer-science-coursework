import os
import re
import json
from typing import List, Dict, Set
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        初始化文档处理器
        :param chunk_size: 文档分块大小
        :param chunk_overlap: 分块重叠大小
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )

    def full_to_half(self, text: str) -> str:
        """
        将全角字符转换为半角字符
        """
        res = []
        for c in text:
            if c == '\u3000':  # 全角空格
                res.append(' ')
            elif 0xFF00 <= ord(c) <= 0xFFEF:
                res.append(chr(ord(c) - 0xfee0))
            else:
                res.append(c)
        return ''.join(res)

    def clean_text(self, text: str) -> str:
        """
        清洗文本内容
        :param text: 原始文本
        :return: 清洗后的文本
        """
        # 移除HTML标签
        text = BeautifulSoup(text, "html.parser").get_text()

        # 全角转半角
        text = self.full_to_half(text)

        # 统一标点符号（替换全角为半角）
        punctuation_mapping = {
            '，': ',', '。': '.', '、': ',', '！': '!', '？': '?', '；': ';', '：': ':',
            '“': '"', '”': '"', '‘': "'", '’': "'", '（': '(', '）': ')', '【': '[', 
            '】': ']', '｛': '{', '｝': '}', '《': '<', '》': '>', '·': '-'
        }
        for full, half in punctuation_mapping.items():
            text = text.replace(full, half)

        # 处理非中文字符之间的换行符（如：a\nb → ab）
        text = re.sub(r'([^\u4e00-\u9FFF])\n([^\u4e00-\u9FFF])', r'\1\2', text)

        # 替换项目符号“•”
        text = text.replace('•', '')

        # 移除所有空格（包括中英文之间的空格）
        text = text.replace(' ', '')

        # 移除特殊字符（如@#$%^等）
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\.,;:!?$$\]{}\'"_\-<>]', '', text)

        # 处理多余空白字符
        text = re.sub(r'[ \t]+', ' ', text)  # 合并多个空格/制表符
        text = re.sub(r'(\n\s*)+\n', '\n\n', text)  # 合并多个换行为一个段落分隔
        text = text.strip()  # 去除首尾空白

        # 修正 Markdown 格式错误
        # 统一标题格式（添加空格）
        text = re.sub(r'^(#+)([^\s])', r'\1 \2', text, flags=re.MULTILINE)
        # 统一列表符号为 "- "（加空格）
        text = re.sub(r'^[\*\+\-]\s*', '- ', text, flags=re.MULTILINE)

        return text

    def load_document(self, file_path: str, verbose: bool = False) -> List[Document]:
        """
        加载单个文档并清洗内容，可选择是否显示清洗前后的内容片段
        :param file_path: 文件路径
        :param verbose: 是否显示清洗前后的内容片段（调试用）
        :return: Document 列表
        """
        file_extension = os.path.splitext(file_path)[1].lower()

        # print(f"检查后缀是否正确：{file_extension}")
        try:
            if file_extension == '.pdf':
                loader = PyPDFLoader(file_path)
            elif file_extension == '.txt':
                loader = TextLoader(file_path, encoding='utf-8-sig')  # 支持 BOM
            elif file_extension == '.md':
                print(f"加载文件: {file_path}")
                # md文件可能会报错，用textloader替代、
                loader = TextLoader(file_path, encoding='utf-8-sig')
            else:
                raise ValueError(f"不支持的文件类型: {file_extension}")

            documents = loader.load()

            # 显示原始内容片段（调试用）
            if verbose and documents:
                print(f"\n【原始内容片段】 - {file_path}")
                print(documents[0].page_content[:200] + "...")  # 打印前200字符

            # 清洗文档内容
            for doc in documents:
                doc.page_content = self.clean_text(doc.page_content)

            # 显示清洗后内容片段（调试用）
            if verbose and documents:
                print(f"\n【清洗后内容片段】 - {file_path}")
                print(documents[0].page_content[:200] + "...")  # 打印前200字符

            return documents

        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {str(e)}")
            return []

    def load_directory(self, directory_path: str, existing_sources: Set[str] = None) -> List[Document]:
        """
        加载目录下的所有未处理的文档。
        :param directory_path: 目录路径。
        :param file_extensions: 要处理的文件扩展名列表。
        :param existing_sources: 已存在的 source 集合（用于去重）。
        :return: Document 列表。
        """
        file_extensions = ['.pdf', '.txt', '.md']

        all_documents = []

        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if any(file.endswith(ext) for ext in file_extensions):
                    # 如果文件已存在于知识库中，跳过
                    print(f"正在处理的文件：{file_path}")
                    if existing_sources and file_path in existing_sources:
                        print(f"文件 {file_path} 已存在于知识库中，跳过处理。")
                        continue

                    # 否则加载文档
                    documents = self.load_document(file_path)
                    all_documents.extend(documents)

        return all_documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        将文档分割成更小的块
        :param documents: Document 列表
        :return: 分割后的 Document 列表
        """
        return self.text_splitter.split_documents(documents)


# 示例用法
if __name__ == "__main__":
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)

    # 处理单个文件
    # file_path = "./documents/利用导数定义求解极限_杨德志.pdf"  # 替换为实际文件路径
    # file_path = "./documents/danggui.md"  # 替换为实际文件路径
    file_path = "./documents/test.txt"  # 替换为实际文件路径

    documents = processor.load_document(file_path,verbose=True)
    split_docs = processor.split_documents(documents)

    print(f"原始文档数量: {len(documents)}")
    print(f"分割后文档数量: {len(split_docs)}")
    # # 处理整个目录
    # directory_path = "path/to/your/documents"  # 替换为实际目录路径
    # all_documents = processor.load_directory(directory_path)
    # all_split_docs = processor.split_documents(all_documents)

    # print(f"目录中原始文档总数: {len(all_documents)}")
    # print(f"目录中分割后文档总数: {len(all_split_docs)}")
