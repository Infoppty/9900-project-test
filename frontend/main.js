const API_BASE = "http://localhost:5000";

let state = {
  sentiment: "all",
  page: 1,
  size: 10,
  total: 0
};

// ======== DOM 元素 ========
const elTotal = document.getElementById("kpi-total");
const elPos   = document.getElementById("kpi-pos");
const elNeg   = document.getElementById("kpi-neg");
const elList  = document.getElementById("list");

// ======== 工具函数 ========
function qs(obj) {
  return new URLSearchParams(
    Object.fromEntries(Object.entries(obj).filter(([_, v]) => v !== "" && v !== undefined))
  ).toString();
}

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

// ======== KPI 加载  ========
async function loadKpis() {
  // TODO: 调用后端 /api/kpis 接口，更新 elTotal / elPos / elNeg
}

// ======== 评论数据加载（目前只请求 all） ========
async function loadReviews() {
  const q = qs({ sentiment: "all" }); 
  const url = `${API_BASE}/api/reviews?${q}`;

  elList.innerHTML = `<div class="text-center text-gray-500 py-8">Loading…</div>`;

  try {
    const data = await fetchJSON(url);
    state.total = data.total || 0;
    renderList(data.items || []); 
  } catch (e) {
    elList.innerHTML = `<div class="text-center text-red-600 py-8">加载失败：${e.message}</div>`;
  }
}

// ======== 渲染评论列表  ========
function renderList(items) {
  if (!items.length) {
    elList.innerHTML = `<div class="text-center text-gray-400 py-8">No data</div>`;
    return;
  }

  elList.innerHTML = items.map(row => `
    <div class="p-4 border-b border-gray-200">
      <div class="text-gray-800">${escapeHTML(row.text || "")}</div>
      <div class="text-gray-400 text-xs mt-1">#${row.id ?? ""} | Sentiment: ${row.sentiment}</div>
    </div>
  `).join("");
}

// ======== HTML 转义工具 ========
function escapeHTML(str) {
  return str.replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

// ======== 初始化入口 ========
(async function boot() {
  await loadKpis();   
  await loadReviews(); 
})();
