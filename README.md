# 论文多维度审查系统

基于 DeepSeek V4 的论文多维度智能审查工具。粘贴论文全文，自动拆分段落、多维度联合审查、生成改写建议。

## 快速开始

```bash
# 1. 克隆项目
git clone git@github.com:YueSe-z/PaperLogicInspector.git
cd PaperLogicInspector

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 API Key
# 将 .env.example 复制为 .env，然后编辑填入 DeepSeek API Key

# 4. 启动
python web_ui.py
# 浏览器打开 http://127.0.0.1:5000
```

## 依赖

- Python >= 3.9
- anthropic >= 0.97.0
- flask >= 1.1.0
- python-dotenv >= 1.0.0

## 使用

### Web 界面

`python web_ui.py` 启动后，浏览器访问 http://127.0.0.1:5000，粘贴论文文本，点击"开始分析"。支持 SSE 实时进度推送。

### 命令行

`python main.py`，逐行粘贴论文内容，输入 `END` 结束。

## 审查维度

| 维度 | 检查内容 |
|------|---------|
| 逻辑审查 | 论点一致性、论据充分性、论证方式正确性、推理链条完整性 |
| 方法论审查 | 方法选择合理性、实施细节、可复现性、局限性、替代方案 |
| 创新性评估 | 研究问题新颖性、与现有工作差异、贡献清晰度、过度声称 |
| 证据审查 | 实验设计、数据质量、统计方法、对照组、混淆因素 |
| 清晰度审查 | 术语定义、逻辑流畅、句子结构、歧义性、摘要结论一致性 |

每个维度配有 Rubric Reviewer 质量门禁，审查不完整时自动重试（最多 2 次）。

## 架构

```
用户输入（长文本）
  → 段落拆分 (paragraph_splitter)
    → 并行段落结构解析 (parser_agent × N paragraphs)
      → 逐维度审查 (5 dimensions, each: Worker → Rubric Reviewer)
        → 改写建议生成 (rewrite_agent, 仅针对有问题的段落)
```

### 目录结构

```
├── agents/              # 8 个专业 Agent
│   ├── base.py          # BaseAgent 基类
│   ├── parser_agent.py  # 段落结构解析
│   ├── logic_agent.py   # 逻辑审查
│   ├── methodology_agent.py
│   ├── novelty_agent.py
│   ├── evidence_agent.py
│   ├── clarity_agent.py
│   ├── rewrite_agent.py # 改写建议
│   └── rubric_reviewer.py # 质量门禁
├── orchestrator/        # 编排层
│   ├── protocols.py     # 数据结构
│   ├── paragraph_splitter.py
│   └── pipeline.py      # 核心流水线
├── api_client.py        # DeepSeek API 调用（Anthropic 兼容端点）
├── config.py            # 环境配置
├── main.py              # CLI 入口
├── web_ui.py            # Flask Web 入口
└── templates/index.html # 前端页面
```

## 配置项

在 `.env` 文件中配置：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `API_KEY` | (必填) | DeepSeek API Key |
| `BASE_URL` | `https://api.deepseek.com/anthropic` | API 地址（DeepSeek Anthropic 兼容端点） |
| `MODEL_NAME` | `deepseek-v4-pro[1m]` | 模型名称 |
| `MAX_PARAGRAPH_CHARS` | `3000` | 段落最大字符数 |
| `MAX_WORKERS` | `6` | 并行解析线程数 |
| `MAX_RUBRIC_RETRIES` | `2` | Rubric 审查最大重试次数 |
