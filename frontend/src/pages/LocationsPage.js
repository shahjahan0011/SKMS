import React, { useState, useEffect } from "react";
import { getUserLocations, saveLocation, deleteLocation } from "../api";

export default function LocationsPage({ session }) {
  const [locations, setLocations] = useState([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    name: "",
    unit: "",
    street: "",
    postal_code: "",
    province: "",
    city: "",
    country: "",
  });

  const load = async () => {
    try {
      const data = await getUserLocations(session.userId);
      setLocations(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => { load(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const payload = {
        unit: Number(form.unit),
        street: form.street,
        postal_code: form.postal_code,
        province: form.province,
        city: form.city,
        country: form.country,
      };
      await saveLocation(session.userId, form.name, payload);
      setForm({ name: "", unit: "", street: "", postal_code: "", province: "", city: "", country: "" });
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (locationId) => {
    try {
      await deleteLocation(locationId);
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <h2 className="page-title">Saved Addresses</h2>
      {error && <div className="error">{error}</div>}

      <div className="card">
        <h3>Add New Address</h3>
        <form onSubmit={handleSubmit}>
          <div className="field"><label>Label</label><input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required /></div>
          <div className="field"><label>Unit</label><input type="number" value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} required /></div>
          <div className="field"><label>Street</label><input value={form.street} onChange={(e) => setForm({ ...form, street: e.target.value })} required /></div>
          <div className="field"><label>City</label><input value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} required /></div>
          <div className="field"><label>Province</label><input value={form.province} onChange={(e) => setForm({ ...form, province: e.target.value })} required /></div>
          <div className="field"><label>Postal Code</label><input value={form.postal_code} onChange={(e) => setForm({ ...form, postal_code: e.target.value })} required /></div>
          <div className="field"><label>Country</label><input value={form.country} onChange={(e) => setForm({ ...form, country: e.target.value })} required /></div>
          <button type="submit">Save Address</button>
        </form>
      </div>

      <div className="card">
        <h3>My Addresses</h3>
        {locations.length === 0 ? (
          <div className="empty">No saved addresses</div>
        ) : (
          locations.map((loc) => (
            <div key={loc.location_id} className="menu-item">
              <div className="info">
                <strong>{loc.name}</strong>
                <div className="meta">{loc.unit} {loc.street}, {loc.city}, {loc.province} {loc.postal_code}, {loc.country}</div>
              </div>
              <button className="danger small" onClick={() => handleDelete(loc.location_id)}>Delete</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}