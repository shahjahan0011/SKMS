import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getMenu, getRestaurant } from "../api";
import { useCart } from "../App";

export default function RestaurantPage({ session }) {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [items, setItems] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [error, setError] = useState("");
  const { addToCart } = useCart();

  const load = async () => {
    setError("");
    try {
      const r = await getRestaurant(id).catch(() => null);
      setRestaurant(r);
      const menu = await getMenu(id, search, page, 10);
      const list = menu.items || menu.menu || menu.data || [];
      setItems(Array.isArray(list) ? list : []);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => { load(); }, [id, page]);

  const handleAdd = (item) => {
    addToCart({ id: item.id || item.item_id, name: item.name, price: Number(item.price) }, id);
  };

  return (
    <div className="container">
      <h2 className="page-title">{restaurant?.name || "Menu"}</h2>
      {restaurant && (
        <div className="card">
          <div className="meta">{restaurant.cuisine} · ★ {restaurant.rating}</div>
        </div>
      )}
      <div className="card">
        <div className="row">
          <input
            placeholder="Search menu..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ flex: 1 }}
          />
          <button onClick={() => { setPage(1); load(); }}>Search</button>
        </div>
      </div>
      {error && <div className="error">{error}</div>}
      <div className="card">
        {items.length === 0 ? (
          <div className="empty">No items found</div>
        ) : (
          items.map((item) => {
            const itemId = item.id || item.item_id;
            const stock = item.stock_count !== undefined ? Number(item.stock_count) : null;
            const outOfStock = stock !== null && stock <= 0;
            return (
              <div key={itemId} className="menu-item">
                <div className="info">
                  <div><strong>{item.name}</strong></div>
                  <div className="meta">{item.description}</div>
                  {stock !== null && (
                    <div className="meta">
                      {outOfStock ? (
                        <span className="badge out-of-stock">Out of stock</span>
                      ) : (
                        <span>Stock: {stock}</span>
                      )}
                    </div>
                  )}
                </div>
                <div className="price">${Number(item.price).toFixed(2)}</div>
                <button onClick={() => handleAdd(item)} disabled={outOfStock}>Add</button>
              </div>
            );
          })
        )}
      </div>
      <div className="row" style={{ justifyContent: "center" }}>
        <button className="secondary" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>Previous</button>
        <span>Page {page}</span>
        <button className="secondary" onClick={() => setPage((p) => p + 1)}>Next</button>
      </div>
    </div>
  );
}