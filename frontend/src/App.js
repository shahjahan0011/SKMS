import { useState } from "react";
import "./App.css";
import { API_BASE_URL } from "./api/client";
import TabBar from "./components/TabBar";
import ResponsePanel from "./components/ResponsePanel";
import BrowseView from "./views/BrowseView";
import AuthView from "./views/AuthView";
import OrdersView from "./views/OrdersView";
import DeliveryView from "./views/DeliveryView";
import NotificationsView from "./views/NotificationsView";
import AdminView from "./views/AdminView";

const TABS = [
  { id: "browse", label: "Browse" },
  { id: "auth", label: "Auth" },
  { id: "orders", label: "Orders" },
  { id: "delivery", label: "Delivery" },
  { id: "notifications", label: "Notifications" },
  { id: "admin", label: "Admin" },
];

function App() {
  const [activeTab, setActiveTab] = useState("browse");
  const [responseData, setResponseData] = useState(null);
  const [error, setError] = useState("");

  const onAction = async (action) => {
    try {
      setError("");
      const result = await action();
      setResponseData(result);
    } catch (err) {
      setError(err.message || "Request failed");
    }
  };

  const viewByTab = {
    browse: <BrowseView onAction={onAction} />,
    auth: <AuthView onAction={onAction} />,
    orders: <OrdersView onAction={onAction} />,
    delivery: <DeliveryView onAction={onAction} />,
    notifications: <NotificationsView onAction={onAction} />,
    admin: <AdminView onAction={onAction} />,
  };

  return (
    <main className="app-shell">
      <header className="app-header">
        <h1>SKMS Food Delivery Frontend</h1>
        <p>Backend base URL: {API_BASE_URL}</p>
      </header>

      <TabBar tabs={TABS} activeTab={activeTab} onTabChange={setActiveTab} />

      <div className="content">{viewByTab[activeTab]}</div>

      <ResponsePanel error={error} responseData={responseData} />
    </main>
  );
}

export default App;
