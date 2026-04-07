const BASE = "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data.detail || data.message || `Request failed (${res.status})`;
    throw new Error(typeof msg === "string" ? msg : JSON.stringify(msg));
  }
  return data;
}

export const register = (username, password, role) =>
  request("/auth/register", { method: "POST", body: JSON.stringify({ username, password, role }) });

export const login = (username, password) =>
  request("/auth/login", { method: "POST", body: JSON.stringify({ username, password }) });

export const browseRestaurants = (keyword = "", page = 1, limit = 10) => {
  const params = new URLSearchParams({ page, limit });
  if (keyword) params.set("keyword", keyword);
  return request(`/restaurants/?${params}`);
};

export const getRestaurant = (id) => request(`/restaurants/${id}`);

export const getMenu = (restaurantId, search = "", page = 1, pageSize = 10) => {
  const params = new URLSearchParams({ page, page_size: pageSize });
  if (search) params.set("search", search);
  return request(`/menus/${restaurantId}?${params}`);
};

export const restockItem = (itemId, addedStock, username) =>
  request(`/menus/${itemId}/restock?username=${encodeURIComponent(username)}`, {
    method: "PATCH",
    body: JSON.stringify({ added_stock: addedStock }),
  });

export const createOrder = (username, items, isPremium = false) =>
  request("/orders/", {
    method: "POST",
    body: JSON.stringify({ username, items, is_premium: isPremium }),
  });

export const getOrder = (orderId) => request(`/orders/${orderId}`);

export const cancelOrder = (orderId) =>
  request(`/orders/${orderId}/cancel`, { method: "PATCH" });

export const updateOrderStatus = (orderId, status) =>
  request(`/orders/${orderId}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });

export const getOrderHistory = (username) => request(`/orders/${username}/history`);

export const getActiveRestaurantOrders = (restaurantId) =>
  request(`/orders/restaurant/${restaurantId}/active`);

export const initiatePayment = (orderId, amount) =>
  request("/payments/initiate", {
    method: "POST",
    body: JSON.stringify({ order_id: orderId, amount }),
  });

export const getDelivery = (orderId) => request(`/deliveries/${orderId}`);

export const getUserDeliveries = (userId) => request(`/deliveries/user/${userId}`);

export const getUserLocations = (userId) => request(`/locations/user/${userId}`);

export const deleteLocation = (locationId) =>
  request(`/locations/${locationId}`, { method: "DELETE" });

export const saveLocation = (userId, name, location) =>
  request(`/locations?user_id=${userId}&name=${encodeURIComponent(name)}`, {
    method: "POST",
    body: JSON.stringify(location),
  });

export const getUserNotifications = (username) =>
  request(`/Notifications/?username=${encodeURIComponent(username)}`);

export const getRoleNotifications = (role, username) =>
  request(`/Notifications/role?role=${encodeURIComponent(role)}&username=${encodeURIComponent(username)}`);

export const createPromo = (username, code, discountPercent, maxUses) =>
  request(`/promos/?username=${encodeURIComponent(username)}`, {
    method: "POST",
    body: JSON.stringify({ code, discount_percent: discountPercent, max_uses: maxUses }),
  });

export const listPromos = (username) =>
  request(`/promos/?username=${encodeURIComponent(username)}`);

export const togglePromo = (code, active, username) =>
  request(`/promos/${code}/active?active=${active}&username=${encodeURIComponent(username)}`, {
    method: "PATCH",
  });

export const deletePromo = (code, username) =>
  request(`/promos/${code}?username=${encodeURIComponent(username)}`, { method: "DELETE" });

export const applyPromo = (code, orderTotal) =>
  request("/promos/apply", {
    method: "POST",
    body: JSON.stringify({ code, order_total: orderTotal }),
  });

export const addFavorite = (userId, restaurantId) =>
  request(`/favorites?user_id=${userId}&restaurant_id=${restaurantId}`, { method: "POST" });

export const removeFavorite = (userId, restaurantId) =>
  request(`/favorites?user_id=${userId}&restaurant_id=${restaurantId}`, { method: "DELETE" });

export const getUserFavorites = (userId) => request(`/favorites/user/${userId}`);

export const createRating = (orderId, restaurantId, username, score, comment) =>
  request("/ratings/", {
    method: "POST",
    body: JSON.stringify({ order_id: orderId, restaurant_id: restaurantId, username, score, comment }),
  });

export const getRestaurantStats = (restaurantId) =>
  request(`/ratings/restaurant/${restaurantId}/stats`);

export const getUserRatings = (username) => request(`/ratings/user/${username}/all`);