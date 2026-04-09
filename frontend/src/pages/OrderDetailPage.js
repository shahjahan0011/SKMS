import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getOrder, cancelOrder, getDelivery, createRating } from "../api";

export default function OrderDetailPage({ session }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);
  const [delivery, setDelivery] = useState(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [score, setScore] = useState(5);
  const [comment, setComment] = useState("");

  const load = async () => {
    try {
      const o = await getOrder(id);
      setOrder(o);
      const d = await getDelivery(id).catch(() => null);
      setDelivery(d);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => { load(); }, [id]);

  const handleCancel = async () => {
    setError("");
    try {
      await cancelOrder(id);
      setSuccess("Order cancelled");
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleRate = async (e) => {
    e.preventDefault();
    setError("");
    try {
      await createRating(id, order.restaurant_id, session.username, score, comment);
      setSuccess("Rating submitted!");
    } catch (err) {
      setError(err.message);
    }
  };

  if (!order) return <div className="container"><div className="empty">Loading...</div></div>;

  const status = (order.status || "pending").toLowerCase();
  const canCancel = status === "pending";
  const canRate = status === "delivered";

  return (
    <div className="container">
      <h2 className="page-title">Order #{order.order_id || order.id}</h2>
      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="card">
        <div className="row" style={{ justifyContent: "space-between" }}>
          <div>
            <div><strong>Status:</strong> <span className={`badge ${status}`}>{status}</span></div>
            <div className="meta">Restaurant: {order.restaurant_id}</div>
          </div>
          <div style={{ fontSize: 20, fontWeight: 700 }}>${Number(order.total || 0).toFixed(2)}</div>
        </div>
      </div>

      <div className="card">
        <h3>Cost Breakdown</h3>
        <div className="breakdown">
          <div className="line"><span>Base cost</span><span>${Number(order.base_cost || 0).toFixed(2)}</span></div>
          <div className="line"><span>Tax</span><span>${Number(order.tax || 0).toFixed(2)}</span></div>
          <div className="line"><span>Delivery fee</span><span>${Number(order.delivery_fee || 0).toFixed(2)}</span></div>
          <div className="line total"><span>Total</span><span>${Number(order.total || 0).toFixed(2)}</span></div>
        </div>
      </div>

      {delivery && (
        <div className="card">
          <h3>Delivery</h3>
          <div className="meta">Status: {delivery.status}</div>
          {delivery.agent_name && <div className="meta">Agent: {delivery.agent_name}</div>}
          {delivery.delivery_location && (
            <div className="meta">
              {delivery.delivery_location.street}, {delivery.delivery_location.city}
            </div>
          )}
        </div>
      )}

      {canCancel && (
        <button className="danger" onClick={handleCancel}>Cancel Order</button>
      )}

      {canRate && (
        <div className="card">
          <h3>Rate this order</h3>
          <form onSubmit={handleRate}>
            <div className="field">
              <label>Score</label>
              <select value={score} onChange={(e) => setScore(Number(e.target.value))}>
                {[1, 2, 3, 4, 5].map((n) => <option key={n} value={n}>{n} ★</option>)}
              </select>
            </div>
            <div className="field">
              <label>Comment</label>
              <textarea value={comment} onChange={(e) => setComment(e.target.value)} rows={3} />
            </div>
            <button type="submit">Submit Rating</button>
          </form>
        </div>
      )}

      <button className="secondary" onClick={() => navigate("/orders")}>Back to Orders</button>
    </div>
  );
}