import React, { useState, useEffect } from "react";
import { getUserNotifications } from "../api";

export default function NotificationsPage({ session }) {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getUserNotifications(session.username)
      .then((data) => setNotifications(data.notifications || []))
      .catch((err) => setError(err.message));
  }, [session.username]);

  return (
    <div className="container">
      <h2 className="page-title">Notifications</h2>
      {error && <div className="error">{error}</div>}
      {notifications.length === 0 ? (
        <div className="empty">No notifications</div>
      ) : (
        <div className="card">
          {notifications.map((n) => (
            <div key={n.id} className="menu-item">
              <div className="info">
                <div>{n.message}</div>
                <div className="meta">{n.event_type} · {n.created_at?.split("T")[0]}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}