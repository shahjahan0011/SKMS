import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { browseRestaurants, getUserFavorites, addFavorite, removeFavorite, getRestaurantStats } from "../api";

export default function BrowsePage({ session }) {
  const [restaurants, setRestaurants] = useState([]);
  const [keyword, setKeyword] = useState("");
  const [page, setPage] = useState(1);
  const [favorites, setFavorites] = useState([]);
  const [stats, setStats] = useState({});
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const load = async () => {
    setError("");
    try {
      const data = await browseRestaurants(keyword, page, 9);
      const list = data.restaurants || data.items || data.data || data || [];
      setRestaurants(Array.isArray(list) ? list : []);
      const favs = await getUserFavorites(session.userId).catch(() => []);
      setFavorites(Array.isArray(favs) ? favs.map((f) => Number(f.restaurant_id || f)) : []);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => { load(); }, [page]);

  useEffect(() => {
    restaurants.forEach(async (r) => {
      const id = r.id || r.restaurant_id;
      if (id && !stats[id]) {
        try {
          const s = await getRestaurantStats(id);
          setStats((prev) => ({ ...prev, [id]: s }));
        } catch {}
      }
    });
  }, [restaurants]);

  const toggleFav = async (e, restaurantId) => {
    e.stopPropagation();
    const id = Number(restaurantId);
    try {
      if (favorites.includes(id)) {
        await removeFavorite(session.userId, id);
        setFavorites((prev) => prev.filter((f) => f !== id));
      } else {
        await addFavorite(session.userId, id);
        setFavorites((prev) => [...prev, id]);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <h2 className="page-title">Browse Restaurants</h2>
      <div className="card">
        <div className="row">
          <input
            placeholder="Search restaurants..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            style={{ flex: 1 }}
          />
          <button onClick={() => { setPage(1); load(); }}>Search</button>
        </div>
      </div>
      {error && <div className="error">{error}</div>}
      {restaurants.length === 0 ? (
        <div className="empty">No restaurants found</div>
      ) : (
        <div className="grid">
          {restaurants.map((r) => {
            const id = r.id || r.restaurant_id;
            const isFav = favorites.includes(Number(id));
            const stat = stats[id];
            return (
              <div key={id} className="card restaurant-card" onClick={() => navigate(`/restaurant/${id}`)}>
                <div className="row" style={{ justifyContent: "space-between" }}>
                  <h3>{r.name}</h3>
                  <button className="fav-btn" onClick={(e) => toggleFav(e, id)}>
                    {isFav ? "★" : "☆"}
                  </button>
                </div>
                <div className="meta">{r.cuisine}</div>
                <div className="meta">
                  <span className="stars">★</span> {r.rating || "N/A"}
                  {stat && stat.total_ratings > 0 && (
                    <span> ({stat.average_rating?.toFixed(1)} from {stat.total_ratings} reviews)</span>
                  )}
                </div>
                {r.is_active === false && <span className="badge cancelled">Closed</span>}
              </div>
            );
          })}
        </div>
      )}
      <div className="row" style={{ justifyContent: "center", marginTop: 20 }}>
        <button className="secondary" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>Previous</button>
        <span>Page {page}</span>
        <button className="secondary" onClick={() => setPage((p) => p + 1)}>Next</button>
      </div>
    </div>
  );
}