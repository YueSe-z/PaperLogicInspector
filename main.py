from agents.parser_agent import parse_paragraph
from agents.logic_agent import check_logic
from agents.rewrite_agent import suggest_rewrite

def main():
    print("=== 论文逻辑审查助手 (MVP) ===")
    print("请输入你的论文段落（输入 END 结束）：")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    user_text = "\n".join(lines)

    if not user_text.strip():
        print("未输入内容，退出。")
        return

    print("\n[1/3] 正在解析段落结构...")
    parsed = parse_paragraph(user_text)
    print("结构分析结果：\n", parsed)

    print("\n[2/3] 正在检查逻辑问题...")
    issues = check_logic(parsed, user_text)
    print("逻辑问题列表：\n", issues)

    if issues.strip() != "未发现明显逻辑问题":
        print("\n[3/3] 正在生成改写建议...")
        rewrite = suggest_rewrite(user_text, issues)
        print("改写建议：\n", rewrite)
    else:
        print("\n未发现逻辑问题，无需改写。")

if __name__ == "__main__":
    main()
