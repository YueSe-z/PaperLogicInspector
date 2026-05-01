import json
import queue
import threading
import traceback

from flask import Flask, render_template, request, jsonify, Response

from orchestrator.pipeline import ReviewPipeline

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
        result = ReviewPipeline().run(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"分析失败: {str(e)}"}), 500


@app.route("/analyze/stream", methods=["POST"])
def analyze_stream():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "请输入论文段落"}), 400

    def generate():
        q = queue.Queue()
        pipeline = ReviewPipeline()

        def on_progress(event):
            q.put(event)

        pipeline.progress_callback = on_progress

        def run_pipeline():
            try:
                result = pipeline.run(text)
                q.put({"event": "complete", "result": result})
            except Exception as e:
                q.put({"event": "error", "error": str(e), "traceback": traceback.format_exc()})

        thread = threading.Thread(target=run_pipeline)
        thread.start()

        while True:
            try:
                event = q.get(timeout=30)
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"
                if event["event"] in ("complete", "error"):
                    break
            except queue.Empty:
                yield f"data: {json.dumps({'event': 'heartbeat'})}\n\n"

        thread.join()

    return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
