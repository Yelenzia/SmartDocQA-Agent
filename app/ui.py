import tempfile
from pathlib import Path
import streamlit as st

from .document_loader import load_document
from .vector_store import DocumentVectorStore
from .qa_agent import QAAgent
from .agent_router import IntentRouter


def init_state():
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "documents" not in st.session_state:
        st.session_state.documents = []
    if "messages" not in st.session_state:
        st.session_state.messages = []


def save_uploaded_file(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp.write(uploaded_file.getbuffer())
    temp.flush()
    temp.close()
    return temp.name


def main():
    st.set_page_config(
        page_title="智能文档问答 Agent",
        page_icon="📚",
        layout="wide"
    )

    init_state()

    st.title("智能文档问答 Agent")
    st.caption("RAG · TF-IDF 检索 · 大语言模型")

    with st.sidebar:
        st.subheader("文档知识库")

        uploaded_files = st.file_uploader(
            "上传 PDF / DOCX / TXT",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )

        if st.button("建立知识库", use_container_width=True):
            if not uploaded_files:
                st.warning("请先上传文档。")
            else:
                documents = []

                with st.spinner("正在解析文档并建立检索索引..."):
                    for uploaded_file in uploaded_files:
                        temp_path = save_uploaded_file(uploaded_file)
                        docs = load_document(temp_path)

                        for doc in docs:
                            doc["source"] = uploaded_file.name

                        documents.extend(docs)

                    vector_store = DocumentVectorStore()
                    vector_store.build(documents)

                    st.session_state.vector_store = vector_store
                    st.session_state.documents = documents
                    st.session_state.messages = []

                st.success(
                    f"知识库建立完成，共解析 {len(documents)} 个文档片段。"
                )

        if st.session_state.documents:
            st.divider()

            if st.button("生成文档摘要", use_container_width=True):
                full_text = "\n".join(
                    doc["text"] for doc in st.session_state.documents
                )
                try:
                    with st.spinner("正在生成摘要..."):
                        agent = QAAgent()
                        summary = agent.summarize(full_text)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": "### 文档摘要\n\n" + summary,
                    })
                except Exception as exc:
                    st.error(str(exc))

            if st.button("清空会话", use_container_width=True):
                st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("请输入你想询问的文档问题...")

    if question:
        if st.session_state.vector_store is None:
            st.warning("请先在左侧上传文档并建立知识库。")
            return

        st.session_state.messages.append({
            "role": "user",
            "content": question,
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            try:
                with st.spinner("Agent 正在分析意图并处理文档..."):
                    agent = QAAgent()
                    intent = IntentRouter().route(question)

                    if intent == "summary":
                        full_text = "\n".join(
                            doc["text"] for doc in st.session_state.documents
                        )
                        answer = agent.summarize(full_text)
                        results = []
                    else:
                        results = st.session_state.vector_store.search(question)
                        answer = agent.answer(
                            question,
                            results,
                            st.session_state.messages[:-1],
                        )

                st.markdown(answer)

                if results:
                    with st.expander("查看检索到的文档片段"):
                        for i, item in enumerate(results, start=1):
                            st.markdown(
                                f"**来源 {i}：{item['source']} "
                                f"· {item['location']} "
                                f"· 相似度 {item['score']:.3f}**"
                            )
                            st.write(item["text"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                })

            except Exception as exc:
                st.error(f"回答生成失败：{exc}")
