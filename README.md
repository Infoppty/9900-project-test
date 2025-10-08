# 📁 Project Structure / 项目结构 #

capstone-project-25t3-9900-f18a-donut/<br>
│<br>
├─ crawler/                   # 🐍 Data collection & cleaning / 数据采集与清洗<br>
│   ├─ crawler.py             # Scrape comments from Reddit, Twitter / 从 Reddit 和 Twitter 爬取评论<br>
│   └─ data_cleaning.py       # Clean raw data -> reviews.csv / 清洗原始数据 -> reviews.csv<br>
│<br>
├─ data/<br>
│   ├─ raw/                   # Raw scraped data / 原始爬取数据<br>
│   │   └─ reviews.csv<br>
│   └─ processed/<br>
│       └─ annotated.csv      # ✅ Annotated data (simulated for Sprint 1) / ✅ 标注数据（Sprint 1 使用仿真数据）<br>
│
├─ backend/<br>
│   ├─ app.py                 # 🚀 Flask API server (KPI + Reviews) / Flask 后端 API（KPI + 评论数据）<br>
│   └─ pipeline.py            # Sentiment labeling + dimension classification / 情感标注与维度分类<br>
│<br>
└─ frontend/<br>
    ├─ index.html             # Entry point with Tailwind & fonts / 前端入口文件<br>
    ├─ src/<br>
    │   ├─ App.jsx            # Main React app with dynamic background / React 主应用（含动态背景）<br>
    │   ├─ components/        # Modularized UI components / 前端组件<br>
    │   │   ├─ Header.jsx<br>
    │   │   ├─ KpiCards.jsx<br>
    │   │   ├─ SentimentTabs.jsx<br>
    │   │   ├─ DimensionFilter.jsx<br>
    │   │   ├─ ReviewsList.jsx<br>
    │   │   └─ Pager.jsx<br>
    │   └─ api.js             # API helper functions / API 调用封装<br>
    ├─ main.jsx               # React root / React 入口<br>
    └─ tailwind.config.js<br>



# 📊 Data Pipeline / 数据处理流程 #

python crawler/crawler.py          # Step 1: Scrape comments / 爬取评论<br>
python crawler/data_cleaning.py    # Step 2: Clean data -> reviews.csv / 清洗数据 -> reviews.csv<br>
python backend/pipeline.py         # Step 3: Label + classify -> annotated.csv / 打标签 + 分类 -> annotated.csv<br>
python backend/app.py              # Step 4: Launch Flask API / 启动 Flask 后端<br>

# ⚙️ Setup & Run / 启动项目 #

## 🐍 Backend / 后端 ##
cd backend<br>
python -m venv .venv<br>
.venv\Scripts\activate   # (Windows)<br>
pip install -r requirements.txt<br>
python app.py<br>

## ⚛️ Frontend / 前端 ##
cd frontend<br>
npm install<br>
npm run dev<br>

📍http://localhost:5173