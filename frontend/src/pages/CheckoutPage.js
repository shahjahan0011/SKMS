import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../App";
import { createOrder, initiatePayment, applyPromo, getUserLocations } from "../api";

export default function CheckoutPage({ session }) {
  const { cart, clearCart } = useCart();
  const navigate = useNavigate();
  const [isPremium, setIsPremium] = useState(false);
  const [promoCode, setPromoCode] = useState("");
  const [promoResult, setPromoResult] = useState(null);
  const [promoError, setPromoError] = useState("");
  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    getUserLocations(session.userId)
      .then((data) => setLocations(Array.isArray(data) ? data : []))
      .catch(() => setLocations([]));
  }, [session.userId]);

  const baseCost = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const tax = baseCost * 0.12;
  const deliveryFee = isPremium || baseCost >= 30 ? 0 : 5;
  const subtotal = baseCost + tax + deliveryFee;
  const finalTotal = promoResult ? promoResult.final_total : subtotal;
  const discount = promoResult ? promoResult.discount_amount : 0;

  const handleApplyPromo = async () => {
    setPromoError("");
    setPromoResult(null);
    if (!promoCode.trim()) {
      setPromoError("Enter a promo code");
      return;
    }
    try {
      const result = await applyPromo(promoCode, subtotal);
      setPromoResult(result);
    } catch (err) {
      setPromoError(err.message);
    }
  };

  const handlePlaceOrder = async () => {
    setError("");
    setSuccess("");
    setProcessing(true);
    try {
      const items = cart.map((c) => ({ id: String(c.id), quantity: c.quantity }));
      const order = await createOrder(session.username, items, isPremium);
      const orderId = order.order_id || order.id;
      await initiatePayment(orderId, finalTotal);
      setSuccess(`Order placed and paid! Redirecting...`);
      clearCart();
      setTimeout(() => navigate(`/orders/${orderId}`), 1500);
    } catch (err) {
      setError(err.message);
    } finally {
      setProcessing(false);
    }
  };

  if (cart.length === 0) {
    return (
      <div className="container">
        <div className="empty">Your cart is empty. <a href="/browse">Browse restaurants</a></div>
      </div>
    );
  }

  return (
    <div className="container">
      <h2 className="page-title">Checkout</h2>

      <div className="card">
        <h3>Order Items</h3>
        {cart.map((item) => (
          <div key={item.id} className="menu-item">
            <div className="info">
              <strong>{item.name}</strong>
              <div className="meta">Qty: {item.quantity} × ${item.price.toFixed(2)}</div>
            </div>
            <div className="price">${(item.price * item.quantity).toFixed(2)}</div>
          </div>
        ))}
      </div>

      <div className="card">
        <h3>Delivery Address</h3>
        {locations.length === 0 ? (
          <div className="meta">No saved addresses. Add one in the Addresses tab, or proceed without.</div>
        ) : (
          <select value={selectedLocation} onChange={(e) => setSelectedLocation(e.target.value)}>
            <option value="">Select an address</option>
            {locations.map((loc) => (
              <option key={loc.location_id} value={loc.location_id}>
                {loc.name} — {loc.street}, {loc.city}
              </option>
            ))}
          </select>
        )}
        <div className="row" style={{ marginTop: 12 }}>
          <label style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 0 }}>
            <input
              type="checkbox"
              checked={isPremium}
              onChange={(e) => setIsPremium(e.target.checked)}
              style={{ width: "auto" }}
            />
            Premium membership (free delivery)
          </label>
        </div>
      </div>

      <div className="card">
        <h3>Promo Code</h3>
        <div className="row">
          <input
            placeholder="Enter promo code"
            value={promoCode}
            onChange={(e) => setPromoCode(e.target.value)}
            style={{ flex: 1, textTransform: "uppercase" }}
          />
          <button onClick={handleApplyPromo}>Apply</button>
        </div>
        {promoError && <div className="error">{promoError}</div>}
        {promoResult && (
          <div className="success">
            Code <strong>{promoResult.code}</strong> applied — {promoResult.discount_percent}% off (saved ${promoResult.discount_amount.toFixed(2)})
          </div>
        )}
      </div>

      <div className="card">
        <h3>Cost Breakdown</h3>
        <div className="breakdown">
          <div className="line"><span>Base cost</span><span>${baseCost.toFixed(2)}</span></div>
          <div className="line"><span>Tax (12%)</span><span>${tax.toFixed(2)}</span></div>
          <div className="line"><span>Delivery fee</span><span>${deliveryFee.toFixed(2)}</span></div>
          {promoResult && (
            <div className="line discount"><span>Promo discount</span><span>−${discount.toFixed(2)}</span></div>
          )}
          <div className="line total"><span>Total</span><span>${finalTotal.toFixed(2)}</span></div>
        </div>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <button onClick={handlePlaceOrder} disabled={processing} style={{ width: "100%", padding: 16, fontSize: 16 }}>
        {processing ? "Processing..." : `Place Order & Pay $${finalTotal.toFixed(2)}`}
      </button>
    </div>
  );
}