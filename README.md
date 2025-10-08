# 📁 Project Structure / 项目结构 #

capstone-project-25t3-9900-f18a-donut/
│
├─ crawler/                   # 🐍 Data collection & cleaning / 数据采集与清洗
│   ├─ crawler.py             # Scrape comments from Reddit, Twitter / 从 Reddit 和 Twitter 爬取评论
│   └─ data_cleaning.py       # Clean raw data -> reviews.csv / 清洗原始数据 -> reviews.csv
│
├─ data/
│   ├─ raw/                   # Raw scraped data / 原始爬取数据
│   │   └─ reviews.csv
│   └─ processed/
│       └─ annotated.csv      # ✅ Annotated data (simulated for Sprint 1) / ✅ 标注数据（Sprint 1 使用仿真数据）
│
├─ backend/
│   ├─ app.py                 # 🚀 Flask API server (KPI + Reviews) / Flask 后端 API（KPI + 评论数据）
│   └─ pipeline.py            # Sentiment labeling + dimension classification / 情感标注与维度分类
│
└─ frontend/
    ├─ index.html             # Entry point with Tailwind & fonts / 前端入口文件
    ├─ src/
    │   ├─ App.jsx            # Main React app with dynamic background / React 主应用（含动态背景）
    │   ├─ components/        # Modularized UI components / 前端组件
    │   │   ├─ Header.jsx
    │   │   ├─ KpiCards.jsx
    │   │   ├─ SentimentTabs.jsx
    │   │   ├─ DimensionFilter.jsx
    │   │   ├─ ReviewsList.jsx
    │   │   └─ Pager.jsx
    │   └─ api.js             # API helper functions / API 调用封装
    ├─ main.jsx               # React root / React 入口
    └─ tailwind.config.js



# 📊 Data Pipeline / 数据处理流程 #

python crawler/crawler.py          # Step 1: Scrape comments / 爬取评论
python crawler/data_cleaning.py    # Step 2: Clean data -> reviews.csv / 清洗数据 -> reviews.csv
python backend/pipeline.py         # Step 3: Label + classify -> annotated.csv / 打标签 + 分类 -> annotated.csv
python backend/app.py              # Step 4: Launch Flask API / 启动 Flask 后端

# ⚙️ Setup & Run / 启动项目 #

## 🐍 Backend / 后端 ##
cd backend
python -m venv .venv
.venv\Scripts\activate   # (Windows)
pip install -r requirements.txt
python app.py

## ⚛️ Frontend / 前端 ##
cd frontend
npm install
npm run dev

### 📍http://localhost:5173 ###