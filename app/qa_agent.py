from typing import List, Dict
from langchain_openai import ChatOpenAI
from .config import settings


SYSTEM_PROMPT = """
你是一个严谨的智能文档问答助手。

回答规则：
1. 主要依据给出的文档上下文回答问题。
2. 如果文档中找不到答案，需要明确说明“根据当前文档无法确定”。
3. 不要编造文档中不存在的事实。
4. 优先使用清晰、简洁的中文。
5. 回答末尾列出本次回答使用到的来源。
"""


class QAAgent:
    def __init__(self):
        if not settings.api_key:
            raise ValueError(
                "未配置 LLM_API_KEY，请复制 .env.example 为 .env 并填写 API Key。"
            )

        self.llm = ChatOpenAI(
            api_key=settings.api_key,
            base_url=settings.base_url,
            model=settings.model,
            temperature=0.2,
        )

    @staticmethod
    def build_context(retrieved_docs: List[Dict]) -> str:
        blocks = []
        for i, doc in enumerate(retrieved_docs, start=1):
            blocks.append(
                f"[来源 {i}]\n"
                f"文件：{doc['source']}\n"
                f"位置：{doc['location']} / 分块 {doc['chunk']}\n"
                f"内容：{doc['text']}"
            )
        return "\n\n".join(blocks)

    def answer(
        self,
        question: str,
        retrieved_docs: List[Dict],
        history: List[Dict] = None,
    ) -> str:
        history = history or []
        context = self.build_context(retrieved_docs)

        history_text = "\n".join(
            f"{item['role']}：{item['content']}"
            for item in history[-6:]
        )

        prompt = f"""
以下是从用户文档中检索到的上下文：

{context}

最近对话：
{history_text}

用户问题：
{question}

请严格依据文档内容回答，并在结尾给出来源。
"""

        response = self.llm.invoke([
            ("system", SYSTEM_PROMPT),
            ("human", prompt),
        ])
        return response.content

    def summarize(self, document_text: str) -> str:
        prompt = f"""
请对下面的文档内容进行结构化总结。

要求：
- 提炼主题
- 提炼关键观点
- 保留重要事实
- 使用中文
- 不要补充文档中不存在的信息

文档：
{document_text[:12000]}
"""
        response = self.llm.invoke([
            ("system", SYSTEM_PROMPT),
            ("human", prompt),
        ])
        return response.content
