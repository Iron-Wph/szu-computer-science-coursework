    with open("res.txt", 'r', encoding='utf-8') as f:
        text = f.read()
    # print(text)
    
    
    # 构造提示词
    prompt = f"""
    以下用三个反引号分隔的产品评论的情感是什么？
    每一行文本代表一条评论。
    用一个单词回答：「正面」或「负面」或 「中性」。
    ```{text}```
    """
    response = get_completion(prompt)
    print("输出:")
    print(response)
    
    # 构造提示词
    prompt = f"""
    以下用三个反引号分隔的每条产品评论主要讨论的话题是什么？
    每一行文本代表一条评论。
    请用简单的词语概括一个话题。
    输出的格式为：[评论编号] : [话题1,话题2, ...]
    ```{text}```
    """
    response = get_completion(prompt)
    print("输出:")
    print(response)
    
    # 构造提示词
    prompt = f"""
    以下用三个反引号分隔的产品评论的情感是什么？
    用一个单词回答：「正面」或「负面」或 「中性」。
    以下用三个反引号分隔的每条产品评论主要讨论的话题是什么？
    每一行文本代表一条评论。
    请用简单的词语概括一个话题。
    请以json格式输出，其中包含以下键:评论原文、情感倾向、话题列表。
    ```{text}```
    """
    response = get_completion(prompt)
    print("输出:")
    print(response)