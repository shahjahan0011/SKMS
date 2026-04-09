# Step by Step Handover Guide

## Installation Instructions

To clone the github repository, do the following command:
```bash
git clone https://github.com/shahjahan0011/SKMS.git
```

## Docker Setup
To run the entire project through docker, do the following command:
```bash
docker compose up --build
```

The backend will open at http://localhost:8000/docs and the frontend will run at http://localhost:3000  

In the case docker doesn’t run properly, do the following set of commands:
```bash
docker compose down
docker compose up --build
```

---

## Backend Setup
This is to install all dependencies and run the backend server.

Open the terminal and do the following:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

This will let you access backend at http://localhost:8000/docs  

---

## Frontend Setup
This installs all dependencies for frontend and runs the frontend server.

For this, open a second terminal and run:
```bash
cd frontend
npm install
npm start
```

This will automatically open frontend at http://localhost:3000  

---

# Dependencies

## System Requirements
- Python: 3.9.6  
- pip: 21.2.4  
- Node.js: v24.14.1  
- npm: 11.11.0  
- Docker: 29.3.1  
- Docker Compose: v5.1.1  

---

## Backend Dependencies
These will be installed automatically upon running:
```bash
pip install -r requirements.txt
```

- FastAPI: 0.128.8  
- Uvicorn: 0.39.0  
- Pydantic: 2.12.5  
- Starlette: 0.49.3  
- HTTPX: 0.28.1  
- pytest: 8.4.2  

---

## Frontend Dependencies
These will be installed automatically upon running:
```bash
npm install
```

- React: 19.2.4  
- React DOM: 19.2.4  
- React Router DOM: 7.14.0  
- React Scripts: 5.0.1  

### Testing Libraries
- @testing-library/react: 16.3.2  
- @testing-library/jest-dom: 6.9.1  
- @testing-library/dom: 10.4.1  
- @testing-library/user-event: 13.5.0  

---

# Maintenance Requirements

There are no configurations of external APIs or services. Account credentials are also not applicable as you can create admin/ manager/ user accounts through our login page. All our data is managed under:

```
backend/app/storage/data/
```

wherein you will see that there are csv files for the following:

- **users.csv** - stores username, password and role. This csv is updated automatically as the user creates an account.  
- **restaurants.csv** - restaurant id, name, cuisine and status on whether the restaurant is active. The values in this csv are predefined.  
- **menus.csv** - stores menu item id, restaurant id, item name, price and stock count. The stock count updates automatically when an order is placed but the rest of the values are predefined.  
- **orders.csv** - stores order id, username, restaurant id, if the order was made by a premium user, base cost, tax, delivery fee, total, status, created at, updated at, cancelled at and delivered at. This is updated automatically when an order is placed.  
- **order_items.csv** - stores order item id, order id, item id, quantity and item price. This is updated automatically when an order is placed.  
- **deliveries.csv** - stores order id, restaurant id, user id, username, unit, street, postal code, province, city, country, status, whether it is an emergency order, agent id and agent name. This is updated automatically when an order is placed.  
- **delivery_agents.csv** - stores agent id, name and whether an agent is available. This is a predefined list of agents that updates the availability of an agent after an order’s status becomes delivered for which the agent is assigned.  
- **locations.csv** - stores location id, user id, name, unit, street, postal code, province, city and country. This list is updated automatically when a logged in user creates an address in their account.  
- **favorites.csv** - stores user id and restaurant id. This list updates automatically when a user adds or removes a restaurant to their list of favorites.  
- **notifications.csv** - stores notification id, user id, role, event type, event key, message, order id and created at. This is updated automatically when a user places an order and the user pays for their order.  
- **ratings.csv** - stores rating id, order id, restaurant id, username, score, comment and created_at. This list is automatically updated when a user rates their order.  
- **food_delivery.csv** - stores extended dataset for delivery analytics. This file is predefined and used for analytical and testing purposes.