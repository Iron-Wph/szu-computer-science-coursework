    prompt_direct = """ 
    一个水果摊有 20 个苹果，卖掉了 5 个，又新进了 15 个。\
        现在水果摊有多少个苹果？请直接给出最终数量。
    """
    response_direct = get_completion(prompt_direct)
    print("\n练习 6.1 输出 (直接提问):")
    print(response_direct)
    
    prompt_cot = """
    一个水果摊有 20 个苹果，卖掉了 5 个，又新进了 15 个。\
        现在水果摊有多少个苹果？让我们一步一步地思考。
    """
    response_cot = get_completion(prompt_cot)
    print("\n练习 6.1 输出 (使用 CoT):")
    print(response_cot)
    
    story_text = """
    在阳光明媚的周六下午，张伟和他的朋友李娜决定去参观位于市中心的科技博物馆。\
    他们在博物馆里看到了许多有趣的展品，特别是关于人工智能和未来交通的部分。\
    参观结束后，他们在附近的公园散步，讨论着刚才看到的展品。
    """
    
    import json

    #  步骤 1
    prompt_step1 = f"""
    从以下文本中提取所有的人物姓名和地点名称。
    将结果格式化为一个 Python 列表，其中每个元素是一个包含 'type'\
    (人物/地点) 和 'name' (名称) 的字典。
    只返回Python类型的字典，无需返回任何其他内容！
    文本：```{story_text}```
    """
    response_step1_str = get_completion(prompt_step1)
    print("\n练习 6.2 输出 (步骤 1 - 提取信息):")
    print(response_step1_str)

    def extract_python_code_blocks(text):
        """
        从文本中提取所有被 ```python 和 ``` 包围的代码块
        :param text: 输入文本
        :return: 匹配到的代码块列表
        """
        import re
        pattern = r'```python(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        # 去除每个匹配结果两端的空白字符
        return [match.strip() for match in matches]

    def parse_entities(response_step1_str):
        """
        解析实体列表，兼容字符串形式的Python列表或直接是Python列表
        :param response_step1_str: 可能是字符串形式的Python列表或直接是列表
        :return: 解析后的实体列表
        """
        if isinstance(response_step1_str, list):
            # 如果已经是列表，直接返回
            return response_step1_str

        try:
            # 先尝试用json解析（更安全）
            return json.loads(response_step1_str)
        except json.JSONDecodeError:
            try:
                return extract_python_code_blocks(response_step1_str)
            except (ValueError, SyntaxError) as e:
                print(f"解析实体列表失败: {e}")
                return []  # 如果解析失败，返回空列表

    # 注意：需要将字符串形式的列表转换为真实的 Python 列表
    # 在实际应用中，需要更健壮的解析方法，这里为了演示简化处理
    extracted_info = parse_entities(response_step1_str)
    print(extracted_info)
    
    
    # 步骤 2
    # 确保 extracted_info 是一个列表且不为空
    if isinstance(extracted_info, list) and extracted_info:
        prompt_step2 = f"""
        根据以下提取的关键信息，为原始文本生成一个简短的摘要（不超过 30 字），摘要应包含这些关键信息。

        关键信息：{extracted_info}
        原始文本：```{story_text}```
        """
        response_step2 = get_completion(prompt_step2)
        print("\n练习 6.2 输出 (步骤 2 - 生成摘要):")
        print(response_step2)
    else:
        print("\n练习 6.2 步骤 2: 未能成功提取或解析关键信息，无法生成摘要。")


















