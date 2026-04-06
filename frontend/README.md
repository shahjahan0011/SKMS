# SKMS Frontend (Milestone 4)

This frontend is a React app that drives the SKMS food-delivery backend through operational UI flows.

## What was added

- Componentized frontend architecture:
  - `src/components`: reusable UI blocks (`Card`, `TabBar`, `ResponsePanel`)
  - `src/views`: workflow screens (`Browse`, `Auth`, `Orders`, `Delivery`, `Notifications`, `Admin`)
  - `src/api/client.js`: shared API client and backend base URL config
- Dedicated **Admin** interface for admin checks and operational monitoring.
- Clear pathways for users to search, find, and interact with backend resources.

## Run locally

From the `frontend` directory:

```bash
npm install
npm start
```

Then open:

- http://localhost:3000

## Connect to backend

By default the app calls:

- `http://localhost:8000`

To override, set:

```bash
REACT_APP_API_BASE_URL=http://localhost:8000 npm start
```

## Build

```bash
npm run build
```

## Test

```bash
npm test -- --watchAll=false
```
