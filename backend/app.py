# Launch Flask server and provide API endpoints for frontend data access

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import pandas as pd
from pathlib import Path

app = Flask(__name__)
CORS(app)

# -------- Path Configuration --------
ROOT_DIR = Path(__file__).resolve().parents[1]  # one level above backend/ is the project root
DATA_DIR = ROOT_DIR / "data"
PROC_DIR = DATA_DIR / "processed"
ANNOTATED_CSV = PROC_DIR / "annotated.csv"


# -------- Utility Functions --------
def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize key columns and types:
    - `sentiment` and `text` must exist
    - Support both `dimension` and `dimensions` (if neither exists, create an empty column)
    """
    m = {c.lower(): c for c in df.columns}
    if "sentiment" not in m or "text" not in m:
        abort(500, description="annotated.csv missing required columns: sentiment or text")

    # Required columns
    df["sentiment"] = df[m["sentiment"]].fillna("").astype(str).str.lower()
    df["text"] = df[m["text"]].fillna("").astype(str)

    # Dimension column: support both names
    if "dimension" in m:
        df["dimension"] = df[m["dimension"]].fillna("").astype(str)
    elif "dimensions" in m:
        df["dimension"] = df[m["dimensions"]].fillna("").astype(str)
    else:
        df["dimension"] = ""

    # Optional columns fallback
    if "id" in m:
        df["id"] = pd.to_numeric(df[m["id"]], errors="coerce")
    if "year" in m:
        df["year"] = pd.to_numeric(df[m["year"]], errors="coerce")
    if "region" in m:
        df["region"] = df[m["region"]].fillna("").astype(str)
    if "source" in m:
        df["source"] = df[m["source"]].fillna("").astype(str)

    return df


def load_annotated() -> pd.DataFrame:
    """Read processed/annotated.csv and normalize it"""
    if not ANNOTATED_CSV.exists():
        abort(404, description="annotated.csv not found. Please run the data pipeline first.")
    df = pd.read_csv(ANNOTATED_CSV)
    return _normalize(df)


def filter_by_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """
    Filter by dimension (case-insensitive, support multiple values separated by ';')
    - No filtering if `dimension` is 'All' or empty
    """
    if not dimension or dimension.lower() == "all":
        return df
    want = dimension.lower()
    return df[df["dimension"].astype(str).str.lower().apply(
        lambda s: want in [x.strip() for x in s.split(";")] if s else False
    )]


# -------- Basic Routes --------
@app.get("/health")
def health():
    """Health check endpoint"""
    return jsonify({"ok": True})


# -------- Business Routes --------
@app.get("/api/reviews")
def api_reviews():
    """
    Get review list with support for filtering by sentiment and dimension + pagination.
    Query params:
      sentiment = all | positive | negative | neutral (default: all)
      dimension = All or one of the defined dimensions (default: All)
      page, size = pagination (default: 1, 10; max size: 100)
    """
    df = load_annotated()

    sentiment = (request.args.get("sentiment") or "all").lower()
    dimension = request.args.get("dimension") or "All"

    # Dimension filter
    df = filter_by_dimension(df, dimension)

    # Sentiment filter
    if sentiment in {"positive", "negative", "neutral"}:
        df = df[df["sentiment"] == sentiment]

    # Pagination
    try:
        page = max(1, int(request.args.get("page", 1)))
        size = min(100, max(1, int(request.args.get("size", 10))))
    except Exception:
        page, size = 1, 10

    start, end = (page - 1) * size, (page - 1) * size + size
    page_df = df.iloc[start:end].copy()

    # Build response
    def to_item(row):
        return {
            "id": int(row["id"]) if "id" in row and pd.notna(row["id"]) else None,
            "text": row["text"],
            "sentiment": row["sentiment"],
            "dimension": row.get("dimension", ""),
            "source": row.get("source", ""),
            "region": row.get("region", ""),
            "year": int(row["year"]) if "year" in row and pd.notna(row["year"]) else None,
        }

    items = [to_item(r) for _, r in page_df.iterrows()]
    return jsonify({
        "total": int(len(df)),
        "page": page,
        "size": size,
        "items": items
    })


@app.get("/api/kpis")
def api_kpis():
    """
    Return KPI counts (eNPS is calculated on the frontend).
    Optional query:
      dimension = All or one of the defined dimensions
    Response:
      total, positive_count, negative_count
    """
    df = load_annotated()
    dimension = request.args.get("dimension") or "All"
    df = filter_by_dimension(df, dimension)

    total = int(len(df))
    pos = int((df["sentiment"] == "positive").sum())
    neg = int((df["sentiment"] == "negative").sum())

    return jsonify({
        "total": total,
        "positive_count": pos,
        "negative_count": neg
    })


# -------- Reserved: Sprint 2/3 future endpoints --------


if __name__ == "__main__":
    # Use 0.0.0.0 for container or LAN access; for local testing visit http://localhost:5000
    app.run(host="0.0.0.0", port=5000, debug=True)
