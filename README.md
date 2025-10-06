[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=20520146&assignment_repo_type=AssignmentRepo)



Sprint 1

./crawler/crawler.py  从reddit和twitter上爬取评论 

./crawler/data_cleaning.py  对爬取的评论进行数据清洗，生成reviews.csv文件放于./data/raw

./backend/pipeline.py  对reviews.csv文件中的每条评论及每行 添加 唯一标识(id)并打标签(positive or negative)，生成processed/annotated.csv

**./data/processed/annotated.csv目前为我用于测试的仿真数据**

./backend/app.py  启动 Flask 服务器并提供前端访问数据的接口 (API)  √已完成

./frontend/index.html  搭建前端基础页面（Tailwind + Vite + React），用于验证后端数据展示   √已完成
./frontend/main.js  展示从本地 CSV 文件（annotated.csv）中读取的评论数据 并显示   √已完成

./frontend/main.js  显示基础 KPI（Total、Positive、Negative）, 提供按情感（sentiment）筛选和分页查看功能


任务细化：
1. Crawler（数据采集）

从公开来源抓取评论
输出：data/raw/reviews.csv

字段示例：
source,region,year,text
Glassdoor,AU,2024,Great collaboration between teams and supportive leadership.

2. Pipeline (数据标注与分析)

输入：data/raw/reviews.csv

步骤：
文本清洗 (去重、去空行、标准化)
加唯一标识符(id)
情感分析 (Positive / Negative / Neutral)

字段示例：
id,source,region,year,text,sentiment
0,Glassdoor,AU,2024,Great collaboration between teams and supportive leadership.,positive

3. Backend + Frontend（展示与交互）

Flask 后端读取 annotated.csv，提供 REST API：
GET /api/kpis – 返回总数、正向数、负向数
GET /api/reviews – 支持分页和 sentiment 筛选
React + Vite 前端展示数据（KPI + 列表 + 分页 + 筛选）



接口定义：
1. KPI 接口

GET /api/kpis
Response:
{
  "total": 10,
  "positive_count": 6,
  "negative_count": 4
}

2. 评论数据接口
GET /api/reviews?sentiment=positive&page=1&size=10

Query 参数：
sentiment: "all" | "positive" | "negative" （默认 "all"）
page: 页码 (默认 1)
size: 每页数量 (默认 10)

Response:
{
  "total": 10,
  "items": [
    {
      "id": 0,
      "text": "Great collaboration between teams.",
      "sentiment": "positive"
    }
  ]
}



项目试运行：

后端
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py

前端：
cd frontend
npm install
npm run dev


http://localhost:5173