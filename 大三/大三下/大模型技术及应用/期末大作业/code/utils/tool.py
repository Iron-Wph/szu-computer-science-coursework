import dashscope
from http import HTTPStatus

def rerank_with_dashscope(query, documents):
    """
    使用 DashScope API 进行文档重排序。
    :param query: 查询字符串。
    :param documents: 文档对象列表，每个对象都应包含 `page_content` 属性。
    :return: 按原始顺序排列的文档相关性分数列表。
    """
    print("使用 DashScope 进行重排序")
    # 提取文档内容并创建符合 DashScope API 要求的格式
    doc_texts = []
    for doc in documents:
        if hasattr(doc, 'page_content'):
            doc_texts.append(doc.page_content)
        else:
            # 如果文档没有 page_content 属性，尝试直接使用文档
            doc_texts.append(str(doc))
    try:
        # 确保有文档可以重排
        if not doc_texts:
            print("没有可重排序的文档")
            return [0.0] * len(documents)
        # 调用 DashScope API
        resp = dashscope.TextReRank.call(
            model="gte-rerank-v2",
            query=query,
            documents=doc_texts,  # 直接传递文本列表
            top_n=len(doc_texts),  # 重排所有文档
            return_documents=True  # 需要返回文档以获取索引和分数
        )
        if resp.status_code == HTTPStatus.OK:
            # 初始化分数列表
            scores = [0.0] * len(documents)
            # 根据实际 API 响应格式处理结果
            if hasattr(resp.output, 'results'):
                # 使用 results 字段
                results = resp.output.results
                for result in results:
                    idx = result.get('index', -1)
                    score = result.get('relevance_score', 0.0)
                    if 0 <= idx < len(scores):
                        scores[idx] = score
            elif hasattr(resp.output, 'documents'):
                # 兼容其他可能的格式
                results = resp.output.documents
                for result in results:
                    idx = result.get('index', -1)
                    score = result.get('relevance_score', 0.0)
                    if 0 <= idx < len(scores):
                        scores[idx] = score
            print(f"rerank_scores: {scores}")
            return scores
        else:
            print(f"DashScope 重排序失败: {resp.status_code} - "
                  f"{getattr(resp, 'message', '未知错误')}")
            return [0.0] * len(documents)
    except Exception as e:
        print(f"调用 DashScope API 时发生异常: {e}")
        # 如果出错，返回一个默认分数列表
        return [0.0] * len(documents)


def text_rerank():
    """
    调用文本重排序模型的示例函数。
    """
    try:
        resp = dashscope.TextReRank.call(
            model="gte-rerank-v2",
            query="什么是文本排序模型",
            documents=[
                "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序",
                "量子计算是计算科学的一个前沿领域",
                "预训练语言模型的发展给文本排序模型带来了新的进展"
            ],
            top_n=10,
            return_documents=True
        )
        if resp.status_code == HTTPStatus.OK:
            print("成功调用 API:")
            print(resp)
            
            # 打印结果结构，帮助调试
            print("\n结果结构:")
            print(f"输出类型: {type(resp.output)}")
            
            # 根据实际 API 响应格式处理结果
            if hasattr(resp.output, 'results'):
                print("找到 results 字段:")
                for result in resp.output.results:
                    print(f"索引: {result.get('index')}, 相关性分数: {result.get('relevance_score')}")
                    if 'document' in result:
                        print(f"文档: {result['document'].get('text', '')}")
            elif hasattr(resp.output, 'documents'):
                print("找到 documents 字段:")
                for doc in resp.output.documents:
                    print(doc)
        else:
            print(f"API 调用失败: {resp.status_code}")
            print(resp)
    except Exception as e:
        print(f"测试函数中发生异常: {e}")


if __name__ == '__main__':
    # 请确保您的 DASHSCOPE_API_KEY 环境变量已设置
    text_rerank()