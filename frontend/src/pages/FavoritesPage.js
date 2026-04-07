import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getUserFavorites, removeFavorite, getRestaurant } from "../api";

export default function FavoritesPage({ session }) {
  const [favorites, setFavorites] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const load = async () => {
    try {
      const favs = await getUserFavorites(session.userId);
      const list = Array.isArray(favs) ? favs : [];
      const enriched = await Promise.all(
        list.map(async (f) => {
          const rid = f.restaurant_id || f;
          const r = await getRestaurant(rid).catch(() => ({ id: rid, name: `Restaurant ${rid}` }));
          return { ...r, restaurant_id: rid };
        })
      );
      setFavorites(enriched);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => { load(); }, []);

  const handleRemove = async (rid) => {
    try {
      await removeFavorite(session.userId, Number(rid));
      load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <h2 className="page-title">My Favorites</h2>
      {error && <div className="error">{error}</div>}
      {favorites.length === 0 ? (
        <div className="empty">No favorites yet. Tap the ☆ on any restaurant to save it.</div>
      ) : (
        <div className="grid">
          {favorites.map((r) => (
            <div key={r.restaurant_id} className="card restaurant-card">
              <h3 onClick={() => navigate(`/restaurant/${r.restaurant_id}`)}>{r.name}</h3>
              <div className="meta">{r.cuisine}</div>
              <div className="meta"><span className="stars">★</span> {r.rating || "N/A"}</div>
              <button className="danger small" onClick={() => handleRemove(r.restaurant_id)}>Remove</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}