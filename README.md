# 论文逻辑审查助手

基于 DeepSeek V4 的论文段落逻辑审查工具，提供**结构拆解 → 逻辑检查 → 改写建议**三步审查流程。

## 快速开始

```bash
# 1. 克隆项目
git clone git@github.com:YueSe-z/PaperLogicInspector.git
cd PaperLogicInspector

# 2. 配置 API Key
cp .env.example .env
# 编辑 .env，将 your-deepseek-api-key 替换为你的 DeepSeek API Key

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动
python web_ui.py
# 浏览器打开 http://127.0.0.1:5000
```

## 依赖

- Python >= 3.9
- anthropic >= 0.97
- Flask >= 3.1
- python-dotenv >= 1.0

## 使用

在页面文本框中粘贴论文段落（支持中英文，可一次输入整篇论文），点击"开始分析"，依次获得：

1. **段落结构拆解** — 论点、论据、论证方式、结论
2. **逻辑问题检查** — 跑题、证据不足、论证错误、推理跳跃
3. **改写建议** — 严谨学术风 + 清晰举例风双版本

## 架构

```
文本 → parser_agent → logic_agent → rewrite_agent → 结果
         (拆结构)       (查逻辑)       (给改写)
```

项目使用 DeepSeek Anthropic 兼容接口，通过 Anthropic SDK 调用 DeepSeek V4 模型。
