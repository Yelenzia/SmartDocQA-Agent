# SmartDocQA-Agent（Windows 稳定版）

一个用于简历展示的中文智能文档问答 Agent。

支持 PDF / DOCX / TXT 文档上传，完成文本解析、分块、相关片段检索，并调用 OpenAI Compatible 大语言模型生成回答与文档摘要。

## 为什么有“稳定版”

为了避免 Windows 下 PyTorch、Transformers、SentenceTransformers、FAISS 版本冲突，本版本将本地检索改为：

**中文字符级 TF-IDF + 余弦相似度**

因此运行时不需要：

- PyTorch
- Transformers
- SentenceTransformers
- FAISS

大语言模型仍通过 OpenAI Compatible API 调用。

## 功能

- PDF / DOCX / TXT 文档解析
- 文本自动分块
- TF-IDF 文档检索
- RAG 文档问答
- Agent 意图路由
- 全文摘要
- 连续对话
- 来源片段展示
- Streamlit Web 界面

## 技术栈

Python / Streamlit / LangChain / scikit-learn / TF-IDF / RAG / LLM

## Windows 启动

你的 Python 路径如果是：

```text
D:\编程环境\python.exe
```

直接双击：

```text
启动项目_稳定版.bat
```

或者 PowerShell 执行：

```powershell
cd "项目目录"
& "D:\编程环境\python.exe" -m pip install -r requirements.txt
& "D:\编程环境\python.exe" -m streamlit run run.py
```

不要用：

```powershell
python run.py
```

这是 Streamlit 项目，应使用 `streamlit run` 启动。

## API 配置

复制 `.env.example` 为 `.env`，填写：

```env
LLM_API_KEY=你的API_KEY
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

如果你使用其他 OpenAI Compatible 服务，修改 BASE_URL 和模型名即可。

## 关于 `nn`

`nn` 不是需要单独安装的依赖。

代码里通常看到的：

```python
from torch import nn
```

或：

```python
import torch.nn as nn
```

其中 `nn` 属于 PyTorch。

如果之前执行过：

```powershell
pip install nn
```

可以运行项目里的：

```text
清理误装nn.bat
```

卸载这个无关的第三方包。

## 简历描述建议

**基于大语言模型的智能文档问答 Agent**

使用 Python、LangChain 与 scikit-learn 实现基于 RAG 的智能文档问答系统，支持 PDF、DOCX、TXT 文档解析、文本分块与相关内容检索；设计意图路由，根据用户请求自动选择文档问答或全文摘要能力，并通过 OpenAI Compatible API 调用大语言模型生成回答，同时展示相关文档来源片段。


## 重要：不要混用多个 Python

如果你执行：

```powershell
pip install streamlit
```

但随后使用另一个 Python，例如：

```powershell
& "C:\Users\Yelen\AppData\Roaming\uv\python\cpython-3.12.12-windows-x86_64-none\python.exe" ...
```

那么前一个 Python 安装的包不会自动出现在后一个 Python 中。

本版本推荐直接双击：

```text
启动_独立环境.bat
```

它会在项目目录创建 `.venv`，所有依赖只安装到这个项目的独立环境，不会修改你原来的 PyTorch / CUDA 环境。
