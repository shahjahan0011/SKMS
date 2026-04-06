import { useState } from "react";
import Card from "../components/Card";
import { apiRequest } from "../api/client";

function NotificationsView({ onAction }) {
  const [username, setUsername] = useState("");
  const [role, setRole] = useState("customer");

  return (
    <div className="grid">
      <Card title="My Notifications">
        <input value={username} onChange={(event) => setUsername(event.target.value)} placeholder="Username" />
        <button onClick={() => onAction(() => apiRequest(`/Notifications?username=${encodeURIComponent(username)}`))}>Get User Notifications</button>
      </Card>

      <Card title="Role Notifications (Admin)">
        <input value={username} onChange={(event) => setUsername(event.target.value)} placeholder="Admin Username" />
        <select value={role} onChange={(event) => setRole(event.target.value)}>
          <option value="customer">customer</option>
          <option value="restaurant_owner">restaurant_owner</option>
          <option value="admin">admin</option>
        </select>
        <button onClick={() => onAction(() => apiRequest(`/Notifications/role?username=${encodeURIComponent(username)}&role=${encodeURIComponent(role)}`))}>Get Role Notifications</button>
      </Card>
    </div>
  );
}

export default NotificationsView;
