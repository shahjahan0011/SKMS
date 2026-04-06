import { useState } from "react";
import Card from "../components/Card";
import { apiRequest } from "../api/client";

function OrdersView({ onAction }) {
  const [createForm, setCreateForm] = useState({ username: "", itemId: "", quantity: "1", isPremium: false });
  const [orderId, setOrderId] = useState("");
  const [newStatus, setNewStatus] = useState("preparing");

  return (
    <div className="grid">
      <Card title="Create Order">
        <input value={createForm.username} onChange={(event) => setCreateForm((p) => ({ ...p, username: event.target.value }))} placeholder="Username" />
        <input value={createForm.itemId} onChange={(event) => setCreateForm((p) => ({ ...p, itemId: event.target.value }))} placeholder="Menu item ID" />
        <input type="number" min="1" value={createForm.quantity} onChange={(event) => setCreateForm((p) => ({ ...p, quantity: event.target.value }))} placeholder="Quantity" />
        <label className="checkbox-row">
          <input type="checkbox" checked={createForm.isPremium} onChange={(event) => setCreateForm((p) => ({ ...p, isPremium: event.target.checked }))} />
          Premium user
        </label>
        <button
          onClick={() =>
            onAction(async () => {
              if (!createForm.username || !createForm.itemId) {
                throw new Error("Username and item ID are required");
              }
              return apiRequest("/orders/", {
                method: "POST",
                body: {
                  username: createForm.username,
                  items: [{ id: createForm.itemId, quantity: Number(createForm.quantity) || 1 }],
                  is_premium: createForm.isPremium,
                },
              });
            })
          }
        >
          Create Order
        </button>
      </Card>

      <Card title="Track & Update Order">
        <input value={orderId} onChange={(event) => setOrderId(event.target.value)} placeholder="Order ID" />
        <div className="actions">
          <button onClick={() => onAction(() => apiRequest(`/orders/${orderId}`))}>Get Order</button>
          <button onClick={() => onAction(() => apiRequest(`/orders/${orderId}/cancel`, { method: "PATCH" }))}>Cancel</button>
        </div>

        <select value={newStatus} onChange={(event) => setNewStatus(event.target.value)}>
          <option value="pending">pending</option>
          <option value="preparing">preparing</option>
          <option value="delivered">delivered</option>
          <option value="paid">paid</option>
          <option value="payment_failed">payment_failed</option>
        </select>
        <button onClick={() => onAction(() => apiRequest(`/orders/${orderId}/status`, { method: "PATCH", body: { status: newStatus } }))}>Update Status</button>
      </Card>

      <Card title="Order History & Payment">
        <input value={createForm.username} onChange={(event) => setCreateForm((p) => ({ ...p, username: event.target.value }))} placeholder="Username for history" />
        <div className="actions">
          <button onClick={() => onAction(() => apiRequest(`/orders/${createForm.username}/history`))}>Get History</button>
          <button onClick={() => onAction(() => apiRequest("/payments/initiate", { method: "POST", body: { order_id: orderId, amount: 20 } }))}>Simulate Payment</button>
        </div>
      </Card>
    </div>
  );
}

export default OrdersView;
