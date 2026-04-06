import { useState } from "react";
import Card from "../components/Card";
import { apiRequest } from "../api/client";

function AdminView({ onAction }) {
  const [adminUser, setAdminUser] = useState("");
  const [restaurantId, setRestaurantId] = useState("");

  return (
    <div className="grid">
      <Card title="Admin Access Check">
        <p>Dedicated admin panel actions to monitor protected endpoints.</p>
        <input value={adminUser} onChange={(event) => setAdminUser(event.target.value)} placeholder="Admin Username" />
        <button onClick={() => onAction(() => apiRequest(`/auth/admin?username=${encodeURIComponent(adminUser)}`))}>Verify Admin Access</button>
      </Card>

      <Card title="Operational Monitoring">
        <input value={restaurantId} onChange={(event) => setRestaurantId(event.target.value)} placeholder="Restaurant ID" />
        <button onClick={() => onAction(() => apiRequest(`/orders/restaurant/${restaurantId}/active`))}>Active Restaurant Orders</button>
        <button onClick={() => onAction(() => apiRequest("/locations"))}>All Locations</button>
      </Card>
    </div>
  );
}

export default AdminView;
