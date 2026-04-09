import React, { useState, createContext, useContext } from "react";
import { Routes, Route, Navigate, Link, useNavigate, useLocation } from "react-router-dom";
import { getSession, clearSession } from "./auth";

import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import BrowsePage from "./pages/BrowsePage";
import RestaurantPage from "./pages/RestaurantPage";
import CartPage from "./pages/CartPage";
import CheckoutPage from "./pages/CheckoutPage";
import OrderHistoryPage from "./pages/OrderHistoryPage";
import OrderDetailPage from "./pages/OrderDetailPage";
import FavoritesPage from "./pages/FavoritesPage";
import LocationsPage from "./pages/LocationsPage";
import NotificationsPage from "./pages/NotificationsPage";
import ManagerOrdersPage from "./pages/ManagerOrdersPage";
import AdminPage from "./pages/AdminPage";

export const CartContext = createContext();
export const useCart = () => useContext(CartContext);

function Nav({ session, onLogout }) {
  const location = useLocation();
  const isActive = (path) => (location.pathname === path ? "active" : "");
  if (!session) return null;
  return (
    <nav className="nav">
      <h1>SKMS</h1>
      <Link to="/browse" className={isActive("/browse")}>Browse</Link>
      <Link to="/cart" className={isActive("/cart")}>Cart</Link>
      <Link to="/orders" className={isActive("/orders")}>Orders</Link>
      <Link to="/favorites" className={isActive("/favorites")}>Favorites</Link>
      <Link to="/locations" className={isActive("/locations")}>Addresses</Link>
      <Link to="/notifications" className={isActive("/notifications")}>Notifications</Link>
      {session.role === "manager" && (
        <Link to="/manager" className={isActive("/manager")}>Manager</Link>
      )}
      {session.role === "admin" && (
        <Link to="/admin" className={isActive("/admin")}>Admin</Link>
      )}
      <span className="spacer" />
      <span className="user">{session.username} ({session.role})</span>
      <button onClick={onLogout}>Logout</button>
    </nav>
  );
}

function Protected({ session, children }) {
  if (!session) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  const [session, setSession] = useState(getSession());
  const [cart, setCart] = useState([]);
  const navigate = useNavigate();

  const handleLogin = (newSession) => {
    setSession(newSession);
    navigate("/browse");
  };

  const handleLogout = () => {
    clearSession();
    setSession(null);
    setCart([]);
    navigate("/login");
  };

  const addToCart = (item, restaurantId) => {
    setCart((prev) => {
      if (prev.length > 0 && prev[0].restaurantId !== restaurantId) {
        if (!window.confirm("Cart contains items from another restaurant. Clear cart?")) return prev;
        return [{ ...item, restaurantId, quantity: 1 }];
      }

      const existing = prev.find((i) => i.id === item.id);

      if (existing) {
        return prev.map((i) =>
          i.id === item.id
            ? { ...i, quantity: i.quantity + 1 }
            : i
        );
      }

      return [...prev, { ...item, restaurantId, quantity: 1 }];
    });
  };

  const removeFromCart = (itemId) => {
    setCart((prev) =>
      prev
        .map((item) =>
          item.id === itemId
            ? { ...item, quantity: item.quantity - 1 }
            : item
        )
        .filter((item) => item.quantity > 0)
    );
  };

  const clearCart = () => setCart([]);

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, clearCart }}>
      <div className="app">
        <Nav session={session} onLogout={handleLogout} />
        <Routes>
          <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
          <Route path="/register" element={<RegisterPage onLogin={handleLogin} />} />
          <Route path="/browse" element={<Protected session={session}><BrowsePage session={session} /></Protected>} />
          <Route path="/restaurant/:id" element={<Protected session={session}><RestaurantPage session={session} /></Protected>} />
          <Route path="/cart" element={<Protected session={session}><CartPage /></Protected>} />
          <Route path="/checkout" element={<Protected session={session}><CheckoutPage session={session} /></Protected>} />
          <Route path="/orders" element={<Protected session={session}><OrderHistoryPage session={session} /></Protected>} />
          <Route path="/orders/:id" element={<Protected session={session}><OrderDetailPage session={session} /></Protected>} />
          <Route path="/favorites" element={<Protected session={session}><FavoritesPage session={session} /></Protected>} />
          <Route path="/locations" element={<Protected session={session}><LocationsPage session={session} /></Protected>} />
          <Route path="/notifications" element={<Protected session={session}><NotificationsPage session={session} /></Protected>} />
          <Route path="/manager" element={<Protected session={session}><ManagerOrdersPage session={session} /></Protected>} />
          <Route path="/admin" element={<Protected session={session}><AdminPage session={session} /></Protected>} />
          <Route path="*" element={<Navigate to={session ? "/browse" : "/login"} replace />} />
        </Routes>
      </div>
    </CartContext.Provider>
  );
}