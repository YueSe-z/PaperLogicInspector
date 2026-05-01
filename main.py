from orchestrator.pipeline import ReviewPipeline


def main():
    print("=== 论文多维度审查系统 ===")
    print("请输入论文内容（输入 END 结束）：")
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)
    text = "\n".join(lines)

    if not text.strip():
        print("未输入内容，退出。")
        return

    pipeline = ReviewPipeline()

    def print_progress(event):
        name = event.get("dimension", "")
        if event["event"] == "split":
            print(f"[进度] 段落拆分完成，共 {event.get('paragraph_count', 0)} 段")
        elif event["event"] == "parse":
            print(f"[进度] 段落结构解析 {event.get('paragraph', 0) + 1}/{event.get('total', 0)}")
        elif event["event"] == "review_worker":
            print(f"[进度] {name} 审查中...")
        elif event["event"] == "review_rubric":
            print(f"[进度] {name} 完成 - {event.get('status', '')}")
        elif event["event"] == "rewrite":
            print(f"[进度] 改写建议生成完成")

    pipeline.progress_callback = print_progress
    result = pipeline.run(text)

    print("\n" + "=" * 50)
    print("审查结果汇总")
    print("=" * 50)

    for name, dim_result in result["dimensions"].items():
        status = dim_result["status"]
        icon = "✓" if status == "DONE" else "⚠" if status == "DONE_WITH_CONCERNS" else "✗"
        print(f"\n{icon} [{name}] 状态: {status}")
        if dim_result["concerns"]:
            for c in dim_result["concerns"]:
                print(f"  注意: {c}")
        print(f"  详情: {dim_result['content'][:300]}...")

    if result["rewrite"].get("rewritten"):
        print("\n[改写建议]")
        print(result["rewrite"]["rewritten"][:500])
    else:
        print("\n未发现需要改写的问题。")


if __name__ == "__main__":
    main()
