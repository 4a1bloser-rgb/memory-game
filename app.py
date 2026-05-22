from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "leaderboard.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/leaderboard/<size>", methods=["GET"])
def get_leaderboard(size):
    data = load_data()
    size = str(size)

    if size not in data:
        data[size] = []

    return jsonify(data[size])


@app.route("/api/leaderboard", methods=["POST"])
def add_score():
    new_score = request.get_json()

    size = str(new_score["size"])
    data = load_data()

    if size not in data:
        data[size] = []

    # ⭐支援毫秒排序
    data[size].append(new_score)

    data[size].sort(key=lambda x: (x.get("timeMs", 999999999), x["moves"]))

    data[size] = data[size][:10]

    save_data(data)

    return jsonify({"success": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)