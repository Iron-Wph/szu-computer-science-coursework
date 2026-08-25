import dashscope
from http import HTTPStatus
import time 
import os
# 定义使用DashScope API进行重排序的函数
def rerank_with_dashscope(query, documents, batch_size=5):
    """使用DashScope API对文档进行重排序"""
    all_scores = []
    
    # 分批处理文档以避免超出API限制
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i+batch_size]
        
        # 准备文档列表
        doc_list = [doc.page_content for doc in batch_docs]
        
        # 调用DashScope重排序API
        resp = dashscope.TextReRank.call(
            model=os.getenv("DASHSCOPE_RERANK_MODEL"),
            query=query,
            documents=doc_list,
            top_n=len(doc_list),
            return_documents=True
        )
        
        if resp.status_code == HTTPStatus.OK:
            # 解析返回的结果
            results = resp.output['results']
            # 按照原始索引排序
            results.sort(key=lambda x: x['index'])
            # 提取分数
            batch_scores = [result['relevance_score'] for result in results]
            all_scores.extend(batch_scores)
        else:
            print(f"API调用错误: {resp}")
            # 回退策略：使用简单的长度作为分数
            batch_scores = [len(doc.page_content) / max(len(d.page_content) for d in batch_docs) 
                          for doc in batch_docs]
            all_scores.extend(batch_scores)
        
        # 添加延迟以避免API速率限制
        time.sleep(0.5)
    
    return all_scores