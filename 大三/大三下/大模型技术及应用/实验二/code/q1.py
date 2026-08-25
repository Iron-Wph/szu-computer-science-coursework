    with open('wb.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    # 构造提示词
    prompt = f"""
    您的任务是在新闻网站中生成对新闻文章的简短摘要。
    请对三个反引号之间的新闻文章进行概括，最多50个字；
    其中《》代表文章标题，# 开头为文章的副标题。
    ```{text}```
    """
    response = get_completion(prompt)
    print("输出:")
    print(response)
    
    # 构造提示词
    prompt = f"""
    您的任务是在新闻网站中提取新闻文章的关键信息.
    请对三个反引号之间的新闻文章进行涉及的人物、机构、地点、事件核心要素等关键信息提取。
    并以json的格式返回，其中包含以下键:人物名称、机构名称、地点名称、事件核心要素。
    ```{text}```
    """
    response = get_completion(prompt)
    print("输出:")
    print(response)
    
    # 构造提示词
    prompt = f"""
    您的任务是在新闻网站中生成对新闻文章的简短摘要。
    请对三个反引号之间的新闻文章进行概括，最多50个字, 并且侧重在活动的积极影响上；
    其中《》代表文章标题，# 开头为文章的副标题。
    ```{text}```
    """
    response = get_completion(prompt)
    print("输出:")
    print(response)