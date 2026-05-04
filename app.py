from flask import Flask, jsonify, request, send_from_directory
from recommender import Recommender
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'movies.csv')

app = Flask(__name__, static_folder='static', static_url_path='/')

# lazy load recommender
recommender = None
def get_recommender():
    global recommender
    if recommender is None:
        recommender = Recommender(DATA_PATH)
    return recommender


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/search')
def search():
    q = request.args.get('query', '')
    if not q:
        return jsonify({'error': 'query parameter required'}), 400
    r = get_recommender()
    results = r.recommend_by_query(q, topn=12)
    return jsonify({'query': q, 'results': results})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
