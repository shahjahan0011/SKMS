import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getOrderHistory } from "../api";

export default function OrderHistoryPage({ session }) {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    getOrderHistory(session.username)
      .then((data) => {
        const list = data.orders || data || [];
        setOrders(Array.isArray(list) ? list : []);
      })
      .catch((err) => setError(err.message));
  }, [session.username]);

  return (
    <div className="container">
      <h2 className="page-title">My Orders</h2>
      {error && <div className="error">{error}</div>}
      {orders.length === 0 ? (
        <div className="empty">No orders yet</div>
      ) : (
        <div className="card">
          <table>
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Total</th>
                <th>Status</th>
                <th>Created</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => {
                const id = order.order_id || order.id;
                const status = (order.status || "pending").toLowerCase();
                return (
                  <tr key={id}>
                    <td>{id}</td>
                    <td>${Number(order.total || 0).toFixed(2)}</td>
                    <td><span className={`badge ${status}`}>{status}</span></td>
                    <td>{order.created_at?.split("T")[0]}</td>
                    <td><button className="small" onClick={() => navigate(`/orders/${id}`)}>View</button></td>
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