import { useState } from "react";
import Card from "../components/Card";
import { apiRequest } from "../api/client";

function DeliveryView({ onAction }) {
  const [deliveryForm, setDeliveryForm] = useState({
    order_id: "",
    restaurant_id: "",
    user_id: "",
    user_name: "",
    delivery_location: "",
    status: "pending",
    is_emergency: false,
  });

  return (
    <div className="grid">
      <Card title="Create & Update Delivery">
        <input value={deliveryForm.order_id} onChange={(event) => setDeliveryForm((p) => ({ ...p, order_id: event.target.value }))} placeholder="Order ID" />
        <input value={deliveryForm.restaurant_id} onChange={(event) => setDeliveryForm((p) => ({ ...p, restaurant_id: event.target.value }))} placeholder="Restaurant ID" />
        <input value={deliveryForm.user_id} onChange={(event) => setDeliveryForm((p) => ({ ...p, user_id: event.target.value }))} placeholder="User ID" />
        <input value={deliveryForm.user_name} onChange={(event) => setDeliveryForm((p) => ({ ...p, user_name: event.target.value }))} placeholder="User Name" />
        <input value={deliveryForm.delivery_location} onChange={(event) => setDeliveryForm((p) => ({ ...p, delivery_location: event.target.value }))} placeholder="Delivery Location" />
        <label className="checkbox-row">
          <input type="checkbox" checked={deliveryForm.is_emergency} onChange={(event) => setDeliveryForm((p) => ({ ...p, is_emergency: event.target.checked }))} />
          Emergency Delivery
        </label>
        <div className="actions">
          <button
            onClick={() =>
              onAction(() =>
                apiRequest("/deliveries", {
                  method: "POST",
                  body: {
                    ...deliveryForm,
                    order_id: Number(deliveryForm.order_id),
                    user_id: Number(deliveryForm.user_id),
                  },
                })
              )
            }
          >
            Create Delivery
          </button>
          <button onClick={() => onAction(() => apiRequest(`/deliveries/${deliveryForm.order_id}`))}>Get by Order</button>
        </div>
      </Card>

      <Card title="Delivery Ops">
        <button onClick={() => onAction(() => apiRequest("/deliveries"))}>List Deliveries</button>
        <button onClick={() => onAction(() => apiRequest(`/deliveries/user/${deliveryForm.user_id}`))}>User Deliveries</button>
        <button onClick={() => onAction(() => apiRequest("/agents/available"))}>Find Available Agent</button>
        <button onClick={() => onAction(() => apiRequest(`/deliveries/${deliveryForm.order_id}/status`, { method: "PATCH", body: { new_status: "delivered" } }))}>Mark Delivered</button>
      </Card>
    </div>
  );
}

export default DeliveryView;
