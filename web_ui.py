from flask import Flask, render_template, request, jsonify
from agents.parser_agent import parse_paragraph
from agents.logic_agent import check_logic
from agents.rewrite_agent import suggest_rewrite

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "请输入论文段落"}), 400

    try:
        structure = parse_paragraph(text)

        issues = check_logic(structure, text)

        if "未发现明显逻辑问题" in issues:
            suggestions = None
        else:
            suggestions = suggest_rewrite(text, issues)

        return jsonify({
            "structure": structure,
            "issues": issues,
            "suggestions": suggestions,
        })
    except Exception as e:
        return jsonify({"error": f"分析失败: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
