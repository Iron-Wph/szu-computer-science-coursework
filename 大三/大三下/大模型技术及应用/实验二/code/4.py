    prompt = f"""
    将以下中文翻译成西班牙语: \
    ```您好，我想订购一个搅拌机。```
    """
    response = get_completion(prompt)
    print("\n练习 4.1 输出:")
    print(response)
    
    prompt = f"""将以下文本翻译成商务信函的格式:
    ```小老弟，我小羊，上回你说咱部门要采购的显示器是多少寸来着？```"""
    response = get_completion(prompt)
    print("\n练习 4.2 输出:")
    print(response)

    data_json = { "resturant employees" :[
        {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
        {"name":"Bob", "email":"bob32@gmail.com"},
        {"name":"Jai", "email":"jai87@gmail.com"}
    ]}

    prompt = f"""将以下Python字典从JSON转换为HTML表格，保留表格标题和列名：{data_json}"""
    response = get_completion(prompt)
    print("\n练习 4.3 输出:")
    print(response)
    # 你可以使用以下代码在 Jupyter Notebook 中显示 HTML 表格
    # from IPython.display import display, HTML
    # display(HTML(response))
    
    text = "This phrase is to cherck chatGPT for spelling abilitty"
    prompt = f"""请校对并更正以下文本，注意纠正文本保持原始语种，无需输出原始文本。
        如果您没有发现任何错误，请说“未发现错误”。
        ```{text}```"""
    response = get_completion(prompt)
    print("\n练习 4.4 输出:")
    print(response)