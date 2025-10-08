async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const getKpis = ({ dimension } = {}) => {
  const q = new URLSearchParams(
    dimension && dimension !== 'All' ? { dimension } : {}
  ).toString();
  return fetch(`/api/kpis${q ? `?${q}` : ''}`).then(r => r.json());
};

export const getReviews = ({ sentiment, page, size, dimension }) => {
  const q = new URLSearchParams({
    sentiment, page, size,
    ...(dimension && dimension !== 'All' ? { dimension } : {}),
  }).toString();
  return fetch(`/api/reviews?${q}`).then(r => r.json());
};

