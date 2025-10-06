# 启动 Flask 服务器并提供前端访问数据的接口 (API)


from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import pandas as pd
from pathlib import Path

app = Flask(__name__)
CORS(app)

# 路径配置
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
PROC_DIR = DATA_DIR / "processed"
ANNOTATED_CSV = PROC_DIR / "annotated.csv"


# ---------- 工具函数 ----------
def load_annotated():
    """加载 annotated.csv 并返回 DataFrame"""
    if not ANNOTATED_CSV.exists():
        abort(404, description="annotated.csv not found. Please run pipeline first.")
    df = pd.read_csv(ANNOTATED_CSV)
    if "sentiment" not in df.columns or "text" not in df.columns:
        abort(500, description="annotated.csv missing required columns: sentiment or text")
    df["sentiment"] = df["sentiment"].fillna("").str.lower()
    return df


# ---------- 基础路由 ----------
@app.get("/health")
def health():
    """健康检查"""
    return jsonify({"ok": True})


@app.get("/api/reviews")
def api_reviews():
    """
    获取评论列表，支持按 sentiment 过滤
    query 参数:
      sentiment=all|positive|negative (默认: all)
    """
    df = load_annotated()

    sentiment = (request.args.get("sentiment") or "all").lower()
    if sentiment in ["positive", "negative"]:
        df = df[df["sentiment"] == sentiment]
    # 如果是 all 或空，则不过滤

    # 分页（可选）
    try:
        page = max(1, int(request.args.get("page", 1)))
        size = min(100, max(1, int(request.args.get("size", 50))))
    except ValueError:
        page, size = 1, 50
    start, end = (page - 1) * size, (page - 1) * size + size

    records = df[["id", "text", "sentiment"]].iloc[start:end].to_dict(orient="records")

    return jsonify({
        "total": int(len(df)),
        "page": page,
        "size": size,
        "items": records
    })


@app.get("/api/kpis")
def api_kpis():
    """
    返回评论统计信息：
    - total 总评论数
    - positive_count 正面数
    - negative_count 负面数
    """
    df = load_annotated()
    total = len(df)
    pos = int((df["sentiment"] == "positive").sum())
    neg = int((df["sentiment"] == "negative").sum())

    return jsonify({
        "total": total,
        "positive_count": pos,
        "negative_count": neg
    })

# ---------- Sprint 2/3 ----------



# ---------- Sprint 2/3 ----------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
