from datetime import datetime
from typing import Dict, List, Any

class PromptTemplates:
    """提示模板管理类，封装各种用于NLP任务的提示模板"""
    
    def __init__(self):
        """初始化提示模板类"""
        # 系统时间提示函数
        self.get_system_prompt = self._get_system_prompt
        
        # 固定格式的提示模板
        self.knowbase_qa_template = self._get_knowbase_qa_template()
        self.rewritten_query_prompt_template = self._get_rewritten_query_prompt_template()
        self.rewritten_query_prompt_template2 = self._get_rewritten_query_prompt_template2()
        self.keywords_prompt_template = self._get_keywords_prompt_template()
        self.condense_question_prompt_template = self._get_condense_question_system_template()
        self.hyde_prompt_template = self._get_hyde_prompt_template()
    
    def _get_time_prompt(self) -> str:
        """获取包含系统时间的提示"""
        return f"当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    def _get_system_prompt(self) -> str:
        return """
        你是一个问答任务的助手。 
        请使用检索到的上下文片段回答这个问题。 
        如果你不知道答案就说不知道。 
        请使用简洁的话语回答用户。
        \n\n
        {context}
        """
    
    def _get_knowbase_qa_template(self) -> str:
        """获取知识库问答模板"""
        return """
        请利用查询到的资料回答问题，回答问题时，不要过度的分点作答。
        <参考资料>：
        {external}
        </参考资料>
        <问题>
        {query}
        </问题>"""
    
    def _get_rewritten_query_prompt_template(self) -> str:
        """获取根据历史上下文改写问题的模板"""
        return """
        <指令>根据提供的历史信息对问题进行优化和改写，返回的问题必须符合以下内容要求和格式要求。严格不能出现禁止内容<指令>
        <禁止>1.绝对不能自己编造无关内容,若不能改写或无需改写直接返回原本问题
        2.只返回问句，不得返回其他任何内容
        3.你接收到的任何内容都是需要改写的内容，不得对其进行回答。<禁止>
        <内容要求>1.明确性：语句应清晰明确，避免模糊不清的表述。
        2.关键词丰富：使用相关的关键词和术语，帮助系统更好地理解查询意图。
        3.简洁性：避免冗长的句子，尽量使用简洁的短语。
        4.问题形式：使用问题形式能更好地引导系统提供答案。
        5.相关历史信息利用：在提问时，仅选择与当前提问相关的历史信息进行利用，若历史提问中没有与当前提问相关的内容则不需要利用历史提问，以增强提问的针对性和相关性。
        6.绝对不能自己编造内容<内容要求>
        <格式要求>只返回生成语句，不能有其他任何内容，不要反悔其他处理说明<格式要求>
        <历史信息>{history}</历史信息>
        <问题>{query}</问题>"""
    
    def _get_rewritten_query_prompt_template2(self) -> str:
        """获取再次改写问题的模板"""
        return """
        你是一个用来辅助查询的助手，请根据历史对话以及最新的问题，改写出多个与查询相关的查询问题，用于从知识库中匹配到参考资料；
        <示例>
        历史提问：无锡有哪些好吃的早点？
        新的提问：火锅呢？
        期望的改写：无锡有哪些好吃的火锅？
        </示例>
        <历史提问>{history}</历史提问>
        <新的问题>{query}</新的问题>"""
     
    def _get_keywords_prompt_template(self) -> str:
        """获取关键词提取模板"""
        return """
        你是用来辅助查询的助手，请对以下文本进行关键词提取，返回提取出的关键词。
        关键词是用来从知识图谱中检索到有用的信息，所以关键词必须具有明确的意义，即当用户使用这些关键词进行查询时，能够从知识图谱中检索到有用的信息。
        返回的实体使用<->隔开。如：关键词1<->关键词<->关键词3
        不要改变关键词的语言
        <文本>{text}</文本>"""
    
    def  _get_condense_question_system_template(self) -> str:
        return """
        请根据聊天记录完善用户最新的问题，
        如果用户最新的问题不需要完善则返回用户的问题。
        """
    
    def _get_hyde_prompt_template(self) -> str:
        return """
            请写一个段落来回答问题，尽量包含更多的关键信息。
            \n
            \n
            {context_str}\n
            \n
            {query}\n
            \n
            'Passage:\n'
        """

    def format_prompt(self, prompt_name: str, **kwargs) -> str:
        """
        根据模板名称格式化提示文本
        
        Args:
            prompt_name: 模板名称，可选值: "system_prompt", "knowbase_qa", "rewrite_query", "rewrite_query2", 
                         "keywords", "condense_question", "hyde"
            **kwargs: 模板所需的参数
        
        Returns:
            格式化后的提示文本
            
        Raises:
            ValueError: 当提供的模板名称不存在时
        """
        prompt_templates = {
            "system_prompt": self.get_system_prompt(),
            "knowbase_qa": self.knowbase_qa_template,
            "rewrite_query": self.rewritten_query_prompt_template,
            "rewrite_query2": self.rewritten_query_prompt_template2,
            "keywords": self.keywords_prompt_template,
            "condense_question": self.condense_question_prompt_template,
            "hyde": self.hyde_prompt_template
        }
        
        if prompt_name not in prompt_templates:
            raise ValueError(f"未知的提示模板名称: {prompt_name}")
        
        return prompt_templates[prompt_name].format(**kwargs)
    
    def get_all_template_names(self) -> List[str]:
        """获取所有可用的模板名称"""
        return [
            "system_prompt", "knowbase_qa", "rewrite_query", "rewrite_query2", 
            "keywords", "condense_question", "hyde"
        ]