import React from "react";
import { useNavigate } from "react-router-dom";
import { useCart } from "../App";

export default function CartPage() {
  const { cart, removeFromCart, clearCart } = useCart();
  const navigate = useNavigate();

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div className="container">
      <h2 className="page-title">Cart</h2>
      {cart.length === 0 ? (
        <div className="empty">Your cart is empty</div>
      ) : (
        <>
          <div className="card">
            {cart.map((item) => (
              <div key={item.id} className="menu-item">
                <div className="info">
                  <strong>{item.name}</strong>
                  <div className="meta">Qty: {item.quantity}</div>
                </div>
                <div className="price">${(item.price * item.quantity).toFixed(2)}</div>
                <button className="secondary small" onClick={() => removeFromCart(item.id)}>Remove</button>
              </div>
            ))}
          </div>
          <div className="card">
            <div className="breakdown">
              <div className="line total">
                <span>Subtotal</span>
                <span>${total.toFixed(2)}</span>
              </div>
            </div>
            <div className="row" style={{ marginTop: 16 }}>
              <button onClick={() => navigate("/checkout")}>Proceed to Checkout</button>
              <button className="secondary" onClick={clearCart}>Clear Cart</button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}