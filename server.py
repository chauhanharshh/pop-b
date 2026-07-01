from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import bcrypt
import jwt
import datetime
import os

app = Flask(__name__)
CORS(app)

SECRET_KEY = "popflix_secret_key_2024"
DB_PATH = "popflix.db"

MOVIES = [
    {"id": 1, "title": "Inception", "genre": "Sci-Fi", "rating": 8.8, "year": 2010,
     "director": "Christopher Nolan", "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page", "Tom Hardy"],
     "overview": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
     "poster": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
     "backdrop": "https://image.tmdb.org/t/p/original/s3TBrRGB1iav7gFOCNx3H31MoES.jpg",
     "duration": "2h 28min", "language": "English"},
    {"id": 2, "title": "Interstellar", "genre": "Sci-Fi", "rating": 8.6, "year": 2014,
     "director": "Christopher Nolan", "cast": ["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain", "Michael Caine"],
     "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
     "poster": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
     "backdrop": "https://image.tmdb.org/t/p/original/xJHokMbljvjADYdit5fK5VQsXEG.jpg",
     "duration": "2h 49min", "language": "English"},
    {"id": 3, "title": "The Dark Knight", "genre": "Action", "rating": 9.0, "year": 2008,
     "director": "Christopher Nolan", "cast": ["Christian Bale", "Heath Ledger", "Aaron Eckhart", "Gary Oldman"],
     "overview": "When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest tests of his life.",
     "poster": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
     "backdrop": "https://image.tmdb.org/t/p/original/hkBaDkMWbLaf8B1lsWsKX7Ew3Xq.jpg",
     "duration": "2h 32min", "language": "English"},
    {"id": 4, "title": "Joker", "genre": "Drama", "rating": 8.4, "year": 2019,
     "director": "Todd Phillips", "cast": ["Joaquin Phoenix", "Robert De Niro", "Zazie Beetz"],
     "overview": "In Gotham City, mentally troubled comedian Arthur Fleck embarks on a downward spiral of revolution and bloody crime.",
     "poster": "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
     "backdrop": "https://image.tmdb.org/t/p/original/f5F4cRhQdUbyVbB5lTNCwXzDqnw.jpg",
     "duration": "2h 2min", "language": "English"},
    {"id": 5, "title": "Parasite", "genre": "Thriller", "rating": 8.5, "year": 2019,
     "director": "Bong Joon-ho", "cast": ["Song Kang-ho", "Lee Sun-kyun", "Cho Yeo-jeong"],
     "overview": "Greed and class discrimination threaten the newly formed relationship between the wealthy Park family and the destitute Kim clan.",
     "poster": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
     "backdrop": "https://image.tmdb.org/t/p/original/TU9NIjwzjoKPwQHoHshkFcQUCG.jpg",
     "duration": "2h 12min", "language": "Korean"},
    {"id": 6, "title": "Avengers: Endgame", "genre": "Action", "rating": 8.4, "year": 2019,
     "director": "Anthony & Joe Russo", "cast": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson"],
     "overview": "The Avengers assemble once more to reverse Thanos's actions and restore balance to the universe.",
     "poster": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
     "backdrop": "https://image.tmdb.org/t/p/original/7RyHsO4yDXtBv1zUU3mTpHeQ0d5.jpg",
     "duration": "3h 1min", "language": "English"},
    {"id": 7, "title": "Dune", "genre": "Sci-Fi", "rating": 8.0, "year": 2021,
     "director": "Denis Villeneuve", "cast": ["Timothée Chalamet", "Zendaya", "Oscar Isaac"],
     "overview": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset.",
     "poster": "https://image.tmdb.org/t/p/w500/d5NXSklpcvgDn2e9ry8uhTSNRVZ.jpg",
     "backdrop": "https://image.tmdb.org/t/p/original/iopYFB1b6Bh7FWZh3onQhph1sih.jpg",
     "duration": "2h 35min", "language": "English"},
    {"id": 8, "title": "Oppenheimer", "genre": "Drama", "rating": 8.9, "year": 2023,
     "director": "Christopher Nolan", "cast": ["Cillian Murphy", "Emily Blunt", "Robert Downey Jr."],
     "overview": "The story of J. Robert Oppenheimer and his role in the development of the atomic bomb during WWII.",
     "poster": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg",
     "backdrop": "https://image.tmdb.org/t/p/original/fm6KqXpk3M2HVveHwCrBSSBaO0V.jpg",
     "duration": "3h", "language": "English"},
]

def get_db():
    # Adding timeout=10 helps avoid "database is locked" during concurrent access
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

# ─── MOVIES ───────────────────────────────────────────
@app.route("/api/movies", methods=["GET"])
def get_movies():
    return jsonify(MOVIES)

@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = next((m for m in MOVIES if m["id"] == movie_id), None)
    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    return jsonify(movie)

# ─── AUTH ─────────────────────────────────────────────
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400
    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    conn = None
    try:
        conn = get_db()
        cursor = conn.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed)
        )
        user_id = cursor.lastrowid
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"message": "Email already registered"}), 409
    finally:
        if conn:
            conn.close()

    token = jwt.encode({
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "token": token,
        "user": {"id": user_id, "name": name, "email": email}
    }), 201

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401
    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"message": "Invalid email or password"}), 401

    token = jwt.encode({
        "user_id": user["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "token": token,
        "user": {"id": user["id"], "name": user["name"], "email": user["email"]}
    })

@app.route("/api/auth/me", methods=["GET"])
def me():
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        conn = get_db()
        user = conn.execute("SELECT id, name, email FROM users WHERE id = ?", (payload["user_id"],)).fetchone()
        conn.close()
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(dict(user))
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except Exception:
        return jsonify({"message": "Invalid token"}), 401

if __name__ == "__main__":
    init_db()
    print("PopFlix backend running on http://localhost:5000")
    app.run(port=5000, debug=True)
