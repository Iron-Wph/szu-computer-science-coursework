from utils.retrieval_qa import RetrievalQA

def chat_demo():
    # 初始化 RetrievalQA 实例
    qa_instance = RetrievalQA()

    # 进行多轮对话
    questions = [
        "《中药学》的作者是谁？",
        "麻黄是什么？",
    ]

    print("=== 开始多轮对话 ===")
    for i, question in enumerate(questions, 1):
        print(f"\n第 {i} 轮对话")
        print(f"用户: {question}")
        result = qa_instance.invoke(question)

        if isinstance(result, dict):
            print(f"助手: {result['answer']}")
        else:
            print(f"助手: {result}")

    print("\n=== 完整对话历史 ===")
    print(qa_instance.get_chat_history())

    # 清空历史记录开始新对话
    print("\n=== 清空历史开始新对话 ===")
    qa_instance.clear_chat_history()
    
    # # 测试网页问答
    # url_question = "这是一个什么网站 https://gymnasium.farama.org/ ？"
    # print(f"\n用户: {url_question}")
    # result = qa_instance.invoke(url_question)
    # if isinstance(result, dict):
    #     print(f"助手: {result['answer']}")
    # else:
    #     print(f"助手: {result}")

if __name__ == "__main__":
    chat_demo()






