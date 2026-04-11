import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


class Recommender:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = pd.DataFrame()
        self.tfidf = None
        self.tfidf_matrix = None
        self._load()

    def _load(self):
        self.df = pd.read_csv(self.csv_path)
        self.df.fillna('', inplace=True)
        # combine fields into a single searchable text
        self.df['combined'] = (self.df['title'].astype(str) + ' ' + self.df['genres'].astype(str) + ' ' + self.df['description'].astype(str)).str.lower()
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['combined'])

    def recommend_by_title(self, title, topn=8):
        title = title.strip().lower()
        matches = self.df[self.df['title'].str.lower() == title]
        if matches.empty:
            return []
        idx = matches.index[0]
        cosine_similarities = linear_kernel(self.tfidf_matrix[idx:idx+1], self.tfidf_matrix).flatten()
        related_indices = cosine_similarities.argsort()[::-1]
        related_indices = [i for i in related_indices if i != idx]
        results = self.df.iloc[related_indices][:topn]
        return results.to_dict(orient='records')

    def recommend_by_query(self, query, topn=8):
        q = query.strip().lower()
        if not q:
            return []

        # exact title match
        title_matches = self.df[self.df['title'].str.lower() == q]
        if not title_matches.empty:
            return self.recommend_by_title(q, topn=topn)

        # genres match
        genre_matches = self.df[self.df['genres'].str.lower().str.contains(q)]
        if not genre_matches.empty:
            return genre_matches.head(topn).to_dict(orient='records')

        # fallback: vectorize query and compute similarity
        q_vec = self.tfidf.transform([q])
        cosine_similarities = linear_kernel(q_vec, self.tfidf_matrix).flatten()
        related_indices = cosine_similarities.argsort()[::-1]
        results = self.df.iloc[related_indices][:topn]
        return results.to_dict(orient='records')


if __name__ == '__main__':
    print('Recommender module. Import and use Recommender("data/movies.csv")')
