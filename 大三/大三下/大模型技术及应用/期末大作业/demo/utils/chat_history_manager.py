from typing import List, Dict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class ChatHistoryManager:
    def __init__(self):
        """
        初始化聊天历史管理器。
        历史记录以列表形式存储，每个元素是一个字典，包含 'role' 和 'content'。
        """
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        """
        向聊天历史中添加一条消息。
        :param role: 消息的发送者，通常是 'user' 或 'assistant'。
        :param content: 消息内容。
        """
        if role not in ["user", "assistant", "system"]:
            raise ValueError("角色必须是 'user'、'assistant' 或 'system'。")
        self.history.append({"role": role, "content": content})
        # print(f"消息已添加: [{role}] {content[:50]}...")

    def get_formatted_history(self) -> str:
        """
        获取格式化后的聊天历史，用于作为提示词的一部分。
        :param include_system_prompt: 是否包含可能存在的系统提示（如果历史记录中包含）。
        :return: 格式化后的聊天历史字符串。
        """
        messages = []
        for msg in self.history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))  # 如果有 SystemMessage 需要导入
        return messages

    def get_messages(self) -> List[Dict[str, str]]:
        """
        获取原始的聊天消息列表。
        :return: 聊天消息列表。
        """
        return self.history

    def clear_history(self):
        """
        清空所有聊天历史记录。
        """
        self.history = []
        print("聊天历史已清空。")

    def get_last_message(self) -> Dict[str, str] or None:
        """
        获取最后一条消息。
        :return: 最后一条消息的字典，如果没有消息则返回 None。
        """
        if self.history:
            return self.history[-1]
        return None
    
 

# 示例用法
if __name__ == "__main__":
    history_manager = ChatHistoryManager()

    print("--- 添加消息 ---")
    history_manager.add_message("system", "你是一个乐于助人的AI助手。")
    history_manager.add_message("user", "你好，有什么可以帮助我的吗？")
    history_manager.add_message("assistant", "你好！很高兴为你服务。")
    history_manager.add_message("user", "RAG系统是什么？")
    history_manager.add_message("assistant", "RAG系统是一种基于检索增强生成（Retrieval-Augmented Generation）的AI系统，它结合了检索和生成两个阶段，以提高回答的准确性和相关性。")
    history_manager.add_message("user", "RAG系统有什么特点？")

    print("\n--- 获取格式化历史记录 ---")
    formatted_history = history_manager.get_formatted_history()
    print(formatted_history)

    print("\n--- 获取原始消息列表 ---")
    messages = history_manager.get_messages()
    for msg in messages:
        print(f"角色: {msg['role']}, 内容: {msg['content'][:30]}...")

    print("\n--- 获取最后一条消息 ---")
    last_msg = history_manager.get_last_message()
    if last_msg:
        print(f"最后一条消息 - 角色: {last_msg['role']}, 内容: {last_msg['content'][:30]}...")

    print("\n--- 清空历史记录 ---")
    history_manager.clear_history()
    print(f"清空后历史记录数量: {len(history_manager.get_messages())}")

    history_manager.add_message("user", "这是新会话的第一条消息。")
    print(history_manager.get_formatted_history()) 