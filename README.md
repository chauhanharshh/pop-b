# 🎬 PopFlix — Full Stack Movie App

A Netflix-style movie streaming platform built with React + Vite (Frontend) and Python Flask (Backend).

---

## 🚀 Setup & Run

### Backend (Python Flask)

```bash
cd popflix-backend

# Install dependencies
pip install flask flask-cors pyjwt bcrypt

# Start server
python server.py
```
Backend runs at: `http://localhost:5000`

---

### Frontend (React + Vite)

```bash
cd popflix-frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```
Frontend runs at: `http://localhost:5173`

---

## 📁 Project Structure

```
popflix-frontend/
├── src/
│   ├── components/
│   │   ├── Navbar.jsx         # Top navigation with search & auth
│   │   ├── Hero.jsx           # Hero carousel section
│   │   ├── MovieCard.jsx      # Reusable movie card
│   │   ├── NewReleases.jsx    # Horizontal scroll + grid view
│   │   ├── Top3.jsx           # Top 3 rated movies
│   │   ├── AuthModal.jsx      # Login / Signup popup
│   │   └── Footer.jsx         # CTA footer
│   ├── pages/
│   │   ├── Home.jsx           # Main home page
│   │   └── MovieDetail.jsx    # Individual movie page
│   ├── context/
│   │   └── AuthContext.jsx    # Global auth state
│   ├── services/
│   │   └── api.js             # Axios API calls
│   └── data/
│       └── movies.js          # Local movie data (fallback)

popflix-backend/
└── server.py                  # Flask API server
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/movies` | Get all movies |
| GET | `/api/movies/:id` | Get single movie |
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/me` | Get current user (requires token) |

---

## ✨ Features

- 🎠 **Auto-rotating Hero Carousel** — changes every 3.5 seconds
- 🔍 **Search** — filter movies by title or genre
- 📂 **Load More** — expand movie grid
- 🏆 **Top 3** — sorted by rating with big rank numbers
- 🔐 **Auth** — JWT-based login/signup with modal popup
- 📱 **Responsive** — works on all screen sizes
- 🎨 **Dark Theme** — Netflix-inspired design

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18, Vite, React Router v6 |
| Styling | Plain CSS with CSS Variables |
| Backend | Python Flask |
| Database | SQLite |
| Auth | JWT (JSON Web Tokens) |
| HTTP | Axios |

---

## 📝 Notes

- Movies use TMDB poster images (no API key needed for images)
- Frontend works standalone even without backend (uses local data)
- JWT tokens stored in localStorage, expire after 30 days
