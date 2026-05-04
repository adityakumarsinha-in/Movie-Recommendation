# Hindi Movie Recommender (Flask)

Simple content-based movie recommendation demo using TF-IDF and cosine similarity.

Structure
- `app.py` — Flask server that serves the frontend and `/api/search` endpoint.
- `recommender.py` — TF-IDF recommender wrapped as `Recommender` class.
- `data/movies.csv` — sample Bollywood movie dataset (id,title,genres,description,year).
- `static/` — frontend HTML/CSS/JS (beautiful red & black theme).
- `requirements.txt` — Python dependencies.

Quick start (Windows)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

Usage
- Search by movie title to get similar-taste recommendations.
- Search by genres or themes (e.g., `action`, `romance`) to get movies in that category.

Next steps
- Replace `data/movies.csv` with a larger dataset for better results.
- Add user ratings + collaborative filtering for personalization.
