    sentiment = "消极的"
    review = f"""
    他们在11月份的季节性销售期间以约49美元的价格出售17件套装，折扣约为一半。\
    但由于某些原因（可能是价格欺诈），到了12月第二周，同样的套装价格全都涨到了70美元到89美元不等。\
    11件套装的价格也上涨了大约10美元左右。\
    虽然外观看起来还可以，但基座上锁定刀片的部分看起来不如几年前的早期版本那么好。\
    不过我打算非常温柔地使用它...（省略部分细节）...大约一年后，电机发出奇怪的噪音，我打电话给客服，但保修已经过期了，所以我不得不再买一个。\
    总的来说，这些产品的总体质量已经下降，因此它们依靠品牌认可和消费者忠诚度来维持销售。\
    货物在两天内到达。
    """

    prompt = f"""
    你是一位客户服务的AI助手。
    你的任务是给一位重要客户发送邮件回复。
    根据客户通过“```”分隔的评价，生成回复以感谢客户的评价。提醒模型使用评价中的具体细节
    用简明而专业的语气写信。
    作为“AI客户代理”签署电子邮件。
    客户评论：
    ```{review}```
    评论情感：{sentiment}
    """
    response = get_completion(prompt, temperature=0) # 使用 temperature=0 保证结果一致性
    print("\n练习 5.1 输出:")
    print(response)

    print("\n练习 5.2 输出 (第一次, T=0.7):")
    response1 = get_completion(prompt, temperature=0.7)
    print(response1)
    print("\n练习 5.2 输出 (第二次, T=0.7):")
    import time
    time.sleep(20) # 等待20秒，避免可能的频率限制
    response2 = get_completion(prompt, temperature=0.7)
    print(response2)