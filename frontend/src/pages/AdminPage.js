import React, { useState, useEffect } from "react";
import {
  listPromos,
  createPromo,
  togglePromo,
  deletePromo,
  restockItem,
  browseRestaurants,
  getRestaurantStats,
  getRoleNotifications,
} from "../api";

export default function AdminPage({ session }) {
  const [tab, setTab] = useState("promos");

  return (
    <div className="container">
      <h2 className="page-title">Admin Dashboard</h2>
      <div className="card">
        <div className="row">
          <button className={tab === "promos" ? "" : "secondary"} onClick={() => setTab("promos")}>Promo Codes</button>
          <button className={tab === "restock" ? "" : "secondary"} onClick={() => setTab("restock")}>Restock Items</button>
          <button className={tab === "restaurants" ? "" : "secondary"} onClick={() => setTab("restaurants")}>Restaurants</button>
          <button className={tab === "notifications" ? "" : "secondary"} onClick={() => setTab("notifications")}>Notifications</button>
        </div>
      </div>

      {tab === "promos" && <PromoManager session={session} />}
      {tab === "restock" && <RestockManager session={session} />}
      {tab === "restaurants" && <RestaurantsAdmin />}
      {tab === "notifications" && <NotificationsAdmin session={session} />}
    </div>
  );
}

function PromoManager({ session }) {
  const [promos, setPromos] = useState([]);
  const [code, setCode] = useState("");
  const [discount, setDiscount] = useState(10);
  const [maxUses, setMaxUses] = useState(0);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const load = async () => {
    setError("");
    try {
      const data = await listPromos(session.username);
      setPromos(data.promos || []);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      await createPromo(session.username, code, Number(discount), Number(maxUses));
      setSuccess(`Promo ${code.toUpperCase()} created`);
      setCode("");
      setDiscount(10);
      setMaxUses(0);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleToggle = async (promoCode, currentlyActive) => {
    try {
      await togglePromo(promoCode, !currentlyActive, session.username);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (promoCode) => {
    if (!window.confirm(`Delete promo ${promoCode}?`)) return;
    try {
      await deletePromo(promoCode, session.username);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <div className="card">
        <h3>Create Promo Code</h3>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        <form onSubmit={handleCreate}>
          <div className="field"><label>Code</label><input value={code} onChange={(e) => setCode(e.target.value)} required style={{ textTransform: "uppercase" }} /></div>
          <div className="field"><label>Discount Percent (1-100)</label><input type="number" min="1" max="100" value={discount} onChange={(e) => setDiscount(e.target.value)} required /></div>
          <div className="field"><label>Max Uses (0 = unlimited)</label><input type="number" min="0" value={maxUses} onChange={(e) => setMaxUses(e.target.value)} required /></div>
          <button type="submit">Create Promo</button>
        </form>
      </div>

      <div className="card">
        <h3>All Promo Codes</h3>
        {promos.length === 0 ? (
          <div className="empty">No promo codes yet</div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Code</th>
                <th>Discount</th>
                <th>Uses</th>
                <th>Max</th>
                <th>Active</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {promos.map((p) => {
                const active = String(p.active).toLowerCase() === "true";
                return (
                  <tr key={p.code}>
                    <td><strong>{p.code}</strong></td>
                    <td>{p.discount_percent}%</td>
                    <td>{p.times_used}</td>
                    <td>{p.max_uses === "0" ? "∞" : p.max_uses}</td>
                    <td><span className={`badge ${active ? "delivered" : "cancelled"}`}>{active ? "Active" : "Inactive"}</span></td>
                    <td>
                      <button className="secondary small" onClick={() => handleToggle(p.code, active)}>
                        {active ? "Deactivate" : "Activate"}
                      </button>
                      {" "}
                      <button className="danger small" onClick={() => handleDelete(p.code)}>Delete</button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}

function RestockManager({ session }) {
  const [itemId, setItemId] = useState("");
  const [addedStock, setAddedStock] = useState(10);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      await restockItem(itemId, Number(addedStock), session.username);
      setSuccess(`Item ${itemId} restocked by ${addedStock}`);
      setItemId("");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="card">
      <h3>Restock Menu Item</h3>
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}
      <form onSubmit={handleSubmit}>
        <div className="field"><label>Item ID</label><input value={itemId} onChange={(e) => setItemId(e.target.value)} required /></div>
        <div className="field"><label>Stock to Add</label><input type="number" min="1" value={addedStock} onChange={(e) => setAddedStock(e.target.value)} required /></div>
        <button type="submit">Restock</button>
      </form>
    </div>
  );
}

function RestaurantsAdmin() {
  const [restaurants, setRestaurants] = useState([]);
  const [stats, setStats] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    browseRestaurants("", 1, 50)
      .then((data) => {
        const list = data.data || data.restaurants || data.items || data || [];
        setRestaurants(Array.isArray(list) ? list : []);
      })
      .catch((err) => setError(err.message));
  }, []);

  const loadStats = async (id) => {
    try {
      const s = await getRestaurantStats(id);
      setStats((prev) => ({ ...prev, [id]: s }));
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="card">
      <h3>All Restaurants</h3>
      {error && <div className="error">{error}</div>}
      <table>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Cuisine</th><th>Rating</th><th>Stats</th></tr>
        </thead>
        <tbody>
          {restaurants.map((r) => {
            const id = r.id || r.restaurant_id;
            const stat = stats[id];
            return (
              <tr key={id}>
                <td>{id}</td>
                <td>{r.name}</td>
                <td>{r.cuisine}</td>
                <td>{r.rating}</td>
                <td>
                  {stat ? (
                    <span>{stat.average_rating?.toFixed(1)} ★ ({stat.total_ratings} reviews)</span>
                  ) : (
                    <button className="small secondary" onClick={() => loadStats(id)}>Load</button>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function NotificationsAdmin({ session }) {
  const [role, setRole] = useState("customer");
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState("");

  const load = async () => {
    setError("");
    try {
      const data = await getRoleNotifications(role, session.username);
      setNotifications(data.notifications || []);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="card">
      <h3>Notifications by Role</h3>
      {error && <div className="error">{error}</div>}
      <div className="row" style={{ marginBottom: 16 }}>
        <select value={role} onChange={(e) => setRole(e.target.value)} style={{ flex: 1 }}>
          <option value="customer">Customer</option>
          <option value="manager">Manager</option>
          <option value="admin">Admin</option>
        </select>
        <button onClick={load}>Load</button>
      </div>
      {notifications.length === 0 ? (
        <div className="empty">No notifications loaded</div>
      ) : (
        notifications.map((n) => (
          <div key={n.id} className="menu-item">
            <div className="info">
              <div>{n.message}</div>
              <div className="meta">{n.event_type} · user: {n.user_id}</div>
            </div>
          </div>
        ))
      )}
    </div>
  );
}