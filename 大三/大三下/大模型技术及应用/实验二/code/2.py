    prod_review = """
    这个熊猫公仔是我给女儿的生日礼物，她很喜欢，去哪都带着。
    公仔很软，超级可爱，面部表情也很和善。但是相比于价钱来说，
    它有点小，我感觉在别的地方用同样的价钱能买到更大的。
    快递比预期提前了一天到货，所以在送给女儿之前，我自己玩了会。
    """
    
    prompt = f"""
    您的任务是从电子商务网站上生成一个产品评论的简短摘要。
    请对三个反引号之间的评论文本进行概括，最多30个字。
    评论: ```{prod_review}```
    """
    response = get_completion(prompt)
    print("\n练习 2.1 输出:")
    print(response)
    
    prompt = f"""
    您的任务是从电子商务网站上生成一个产品评论的简短摘要。
    请对三个反引号之间的评论文本进行概括，最多30个字，并且侧重在快递服务上。
    评论: ```{prod_review}```
    """
    response = get_completion(prompt)
    print("\n练习 2.2 输出:")
    print(response)
    
    prompt = f"""
    您的任务是从电子商务网站上的产品评论中提取相关信息。
    请从以下三个反引号之间的评论文本中提取产品运输相关的信息，最多30个词汇。
    评论: ```{prod_review}```
    """
    response = get_completion(prompt)
    print("\n练习 2.3 输出:")
    print(response)