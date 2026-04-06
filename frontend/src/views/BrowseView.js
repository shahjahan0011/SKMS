import { useState } from "react";
import Card from "../components/Card";
import { apiRequest } from "../api/client";

function BrowseView({ onAction }) {
  const [keyword, setKeyword] = useState("");
  const [restaurantId, setRestaurantId] = useState("");
  const [menuSearch, setMenuSearch] = useState("");

  return (
    <div className="grid">
      <Card title="Search Restaurants">
        <p>Find restaurants by keyword and paginate results from the backend.</p>
        <input value={keyword} onChange={(event) => setKeyword(event.target.value)} placeholder="burger, sushi, vegan" />
        <button
          onClick={() =>
            onAction(async () => {
              const query = new URLSearchParams({ page: "1", limit: "10" });
              if (keyword.trim()) query.set("keyword", keyword.trim());
              return apiRequest(`/restaurants?${query.toString()}`);
            })
          }
        >
          Search Restaurants
        </button>
      </Card>

      <Card title="Browse Restaurant Menu">
        <p>Load a single restaurant menu and filter by item text.</p>
        <input value={restaurantId} onChange={(event) => setRestaurantId(event.target.value)} placeholder="Restaurant ID" />
        <input value={menuSearch} onChange={(event) => setMenuSearch(event.target.value)} placeholder="Optional item search" />
        <button
          onClick={() =>
            onAction(async () => {
              if (!restaurantId.trim()) {
                throw new Error("Restaurant ID is required for menu browsing");
              }
              const query = new URLSearchParams({ page: "1", page_size: "10" });
              if (menuSearch.trim()) query.set("search", menuSearch.trim());
              return apiRequest(`/restaurants/${restaurantId.trim()}/menu?${query.toString()}`);
            })
          }
        >
          Get Menu
        </button>
      </Card>
    </div>
  );
}

export default BrowseView;
