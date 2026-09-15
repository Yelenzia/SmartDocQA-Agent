from typing import Literal
from langchain_openai import ChatOpenAI
from .config import settings


class IntentRouter:
    """根据用户问题选择文档问答或全文摘要工具。"""

    def __init__(self):
        if not settings.api_key:
            raise ValueError("未配置 LLM_API_KEY。")

        self.llm = ChatOpenAI(
            api_key=settings.api_key,
            base_url=settings.base_url,
            model=settings.model,
            temperature=0,
        )

    def route(self, question: str) -> Literal["qa", "summary"]:
        prompt = f"""
你是文档 Agent 的意图路由器。

只允许返回一个单词：
- qa：用户希望根据文档回答具体问题、查找事实、解释内容
- summary：用户希望总结、概括、提炼整份文档

用户问题：
{question}

只返回 qa 或 summary。
"""
        result = self.llm.invoke(prompt).content.strip().lower()
        return "summary" if "summary" in result else "qa"
