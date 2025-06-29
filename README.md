Aber natürlich, Michael – hier ist eine saubere, strukturierte `README.md`, die dein **MoviWeb Flask-Projekt** beschreibt. Du kannst sie direkt verwenden oder bei Bedarf noch ergänzen:

---

### ✅ `README.md`

````markdown
# 🎬 MoviWeb – A Personal Movie Tracker

MoviWeb is a lightweight Flask app that lets you manage favorite movies for multiple users. Movies can be added manually or fetched via the OMDb API.

---

## 🚀 Features

- Add, edit, and delete users
- Manage a personalized list of favorite movies per user
- Fetch movie details (title, director, year, poster) from OMDb
- Clean, mobile-friendly UI with simple CSS styling
- SQLite database with SQLAlchemy ORM

---

## 🛠️ Tech Stack

- Python 3.10+
- Flask
- SQLAlchemy
- Requests
- OMDb API

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/moviweb.git
   cd moviweb
````

2. **(Optional) Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   python app.py
   ```

5. Open in your browser: [http://localhost:5000](http://localhost:5000)

---

## 🔑 OMDb API Key

The OMDb API key is currently hardcoded in `data_manager.py`. You can get your own free key at [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx).

To keep it secure, consider using an environment variable or `.env` file in production.

---

## 📁 Project Structure

```
moviweb/
│
├── app.py
├── models.py
├── data_manager.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── edit_user.html
│   ├── movies.html
│   ├── edit_movie.html
│   └── add_from_api.html
├── static/
│   └── styles.css
└── movies.db  ← generated on first run
```

---

## ✅ License

This project is open source and free to use for personal or educational purposes.

```

