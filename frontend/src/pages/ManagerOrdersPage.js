import React, { useState } from "react";
import { getActiveRestaurantOrders, updateOrderStatus } from "../api";

const STATUSES = ["pending", "paid", "preparing", "in-transit", "delivered", "cancelled"];

export default function ManagerOrdersPage() {
  const [restaurantId, setRestaurantId] = useState("");
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const load = async () => {
    setError("");
    try {
      const data = await getActiveRestaurantOrders(restaurantId);
      const list = data.orders || data || [];
      setOrders(Array.isArray(list) ? list : []);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleStatusChange = async (orderId, newStatus) => {
    setError("");
    setSuccess("");
    try {
      await updateOrderStatus(orderId, newStatus);
      setSuccess(`Order ${orderId} updated to ${newStatus}`);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <h2 className="page-title">Manager Dashboard</h2>

      <div className="card">
        <h3>Load Active Orders</h3>
        <div className="row">
          <input
            placeholder="Restaurant ID"
            value={restaurantId}
            onChange={(e) => setRestaurantId(e.target.value)}
            style={{ flex: 1 }}
          />
          <button onClick={load}>Load Orders</button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      {orders.length === 0 ? (
        <div className="empty">No active orders. Enter a restaurant ID and click Load.</div>
      ) : (
        <div className="card">
          <table>
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Total</th>
                <th>Status</th>
                <th>Update Status</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => {
                const id = order.order_id || order.id;
                const status = (order.status || "pending").toLowerCase();
                return (
                  <tr key={id}>
                    <td>{id}</td>
                    <td>{order.username}</td>
                    <td>${Number(order.total || 0).toFixed(2)}</td>
                    <td><span className={`badge ${status}`}>{status}</span></td>
                    <td>
                      <select value={status} onChange={(e) => handleStatusChange(id, e.target.value)}>
                        {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                      </select>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}