import { useState } from "react";
import Card from "../components/Card";
import { apiRequest } from "../api/client";

function AuthView({ onAction }) {
  const [registerForm, setRegisterForm] = useState({ username: "", password: "", role: "customer" });
  const [loginForm, setLoginForm] = useState({ username: "", password: "" });

  return (
    <div className="grid">
      <Card title="Register">
        <input value={registerForm.username} onChange={(event) => setRegisterForm((p) => ({ ...p, username: event.target.value }))} placeholder="Username" />
        <input type="password" value={registerForm.password} onChange={(event) => setRegisterForm((p) => ({ ...p, password: event.target.value }))} placeholder="Password" />
        <select value={registerForm.role} onChange={(event) => setRegisterForm((p) => ({ ...p, role: event.target.value }))}>
          <option value="customer">Customer</option>
          <option value="restaurant_owner">Restaurant Owner</option>
          <option value="admin">Admin</option>
        </select>
        <button onClick={() => onAction(() => apiRequest("/auth/register", { method: "POST", body: registerForm }))}>Register</button>
      </Card>

      <Card title="Login / Logout">
        <input value={loginForm.username} onChange={(event) => setLoginForm((p) => ({ ...p, username: event.target.value }))} placeholder="Username" />
        <input type="password" value={loginForm.password} onChange={(event) => setLoginForm((p) => ({ ...p, password: event.target.value }))} placeholder="Password" />
        <div className="actions">
          <button onClick={() => onAction(() => apiRequest("/auth/login", { method: "POST", body: loginForm }))}>Login</button>
          <button onClick={() => onAction(() => apiRequest("/auth/logout", { method: "POST" }))}>Logout</button>
        </div>
      </Card>
    </div>
  );
}

export default AuthView;
