from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# ⭐排行榜資料檔
DATA_FILE = "leaderboard.json"


# =========================
# 📌 讀取資料
# =========================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# 📌 存資料
# =========================
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# =========================
# 🌐 首頁
# =========================
@app.route("/")
def index():
    return render_template("index.html")


# =========================
# 📊 取得排行榜
# =========================
@app.route("/api/leaderboard/<size>", methods=["GET"])
def get_leaderboard(size):
    data = load_data()

    size = str(size)

    if size not in data:
        data[size] = []

    return jsonify(data[size])


# =========================
# ➕ 新增成績
# =========================
@app.route("/api/leaderboard", methods=["POST"])
def add_score():
    new_score = request.json

    size = str(new_score["size"])

    data = load_data()

    if size not in data:
        data[size] = []

    # ⭐加入新成績
    data[size].append(new_score)

    # ⭐排序（時間優先，其次步數）
    data[size].sort(key=lambda x: (x["seconds"], x["moves"]))

    # ⭐只保留前10名
    data[size] = data[size][:10]

    save_data(data)

    return jsonify({"success": True})


# =========================
# 🚀 Render 用（重要）
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)