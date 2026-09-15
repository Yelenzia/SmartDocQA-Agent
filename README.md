# SmartDocQA-Agent 智能文档问答系统

SmartDocQA-Agent 是一个基于 Python、Streamlit 和大语言模型接口构建的智能文档问答系统。

项目支持 PDF、DOCX、TXT 文档解析，可自动完成文本清洗、分块、内容检索、多轮问答与文档摘要，并通过意图路由模块判断用户需求，在文档问答与全文摘要之间选择对应处理流程。

## 主要功能

- 支持 PDF、DOCX、TXT 文档解析
- 自动进行文本清洗与分块
- 基于字符级 TF-IDF 建立文档检索索引
- 使用余弦相似度对相关文档片段进行排序
- 基于 RAG 的文档问答
- 自动识别“文档问答 / 全文摘要”两类用户意图
- 支持多轮对话上下文
- 回答时展示相关文档来源片段
- 提供 Streamlit 可视化交互界面
- 支持 OpenAI 兼容格式的大语言模型接口

## 系统流程

```text
上传文档
   |
   v
文档解析
   |
   v
文本清洗与分块
   |
   v
建立 TF-IDF 索引
   |
   v
用户输入问题
   |
   v
意图路由
  /     \
 v       v
文档问答  全文摘要
  |       |
  v       v
相关内容检索  文档全文
   \      /
    v    v
   大语言模型
       |
       v
    生成回答
```

## 技术栈

- Python
- Streamlit
- LangChain OpenAI
- scikit-learn
- NumPy
- TF-IDF
- 余弦相似度
- RAG 检索增强生成
- OpenAI 兼容模型接口

## 项目结构

```text
SmartDocQA-Agent/
├── app/
│   ├── __init__.py
│   ├── agent_router.py       # 用户意图路由
│   ├── config.py             # 项目配置读取
│   ├── document_loader.py    # 文档解析
│   ├── qa_agent.py           # 问答与摘要逻辑
│   ├── ui.py                 # Streamlit 交互界面
│   └── vector_store.py       # 文本分块与检索
├── data/                     # 本地数据目录
├── .env.example              # 环境变量示例
├── .gitignore
├── requirements.txt          # Python 项目依赖
├── run.py                    # 项目入口
└── sample_document.txt       # 示例文档
```

## 安装方式

克隆项目：

```bash
git clone https://github.com/Yelenzia/SmartDocQA-Agent.git
cd SmartDocQA-Agent
```

安装依赖：

```bash
pip install -r requirements.txt
```

## 模型配置

将 `.env.example` 复制为 `.env`，然后填写模型接口配置：

```env
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
TOP_K=4
CHUNK_SIZE=500
CHUNK_OVERLAP=80
```

如果使用其他兼容 OpenAI 接口格式的模型服务，只需要修改 `LLM_BASE_URL` 和 `LLM_MODEL` 即可。

## 启动项目

执行：

```bash
python -m streamlit run run.py
```

启动成功后，在浏览器访问：

```text
http://localhost:8501
```

## 文档检索原理

系统首先将上传的文档解析为文本，并按照指定长度切分为存在一定重叠区域的文本块。

随后使用字符级 TF-IDF 对文本块建立索引。当用户提出问题时，系统会对问题进行相同的特征表示，并通过余弦相似度计算用户问题与各文本块之间的相关程度，从中选出最相关的若干片段。

检索出的文档上下文会与用户问题、最近对话历史一起发送给大语言模型，由模型在文档内容基础上生成最终回答，并保留对应的来源信息。

## 意图路由

系统通过独立的意图路由模块判断用户当前需求，目前支持两种处理方式：

- `qa`：针对具体问题检索相关文档片段，并结合文档内容生成回答
- `summary`：读取当前文档内容并生成结构化摘要

通过路由机制，不同类型的请求可以进入不同处理流程，而不需要为每种功能单独建立页面或入口。

## 支持的文件格式

| 文件格式 | 解析方式 |
| --- | --- |
| PDF | PyPDF |
| DOCX | python-docx |
| TXT | UTF-8 文本读取 |

## 配置说明

`TOP_K`：每次问答时检索的相关文本块数量。

`CHUNK_SIZE`：单个文本块的最大字符数。

`CHUNK_OVERLAP`：相邻文本块之间保留的重叠字符数，用于减少文本切分造成的上下文丢失。

## 使用说明

1. 启动项目后，在左侧上传 PDF、DOCX 或 TXT 文档。
2. 点击“建立知识库”，系统会自动解析并建立检索索引。
3. 在底部输入问题，即可根据文档内容进行问答。
4. 可以展开回答下方的相关内容，查看本次回答检索到的文档片段。
5. 需要对整份文档进行概括时，可以直接提出总结类问题，也可以使用文档摘要功能。

## 注意事项

- `.env` 已加入忽略规则，请勿将真实 API Key 上传到代码仓库。
- 上传的文档会先在本地完成解析与检索，再将与当前问题相关的上下文发送给所配置的大语言模型接口。
- 当前检索模块采用 TF-IDF 与余弦相似度实现，后续可以在不修改上层问答逻辑的情况下替换为基于 Embedding 的向量检索方案。
