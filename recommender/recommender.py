# simple recommender using an online dataset link
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend_roles(extracted_skills, dataset_url, top_k=5):
    if not extracted_skills:
        return []

    df = pd.read_csv(dataset_url)
    df["skills"] = df["skills"].fillna("")

    documents = df["skills"].tolist()
    roles = df["role"].tolist()

    resume_doc = " ".join([s.lower() for s in extracted_skills])
    docs = documents + [resume_doc]

    vectorizer = TfidfVectorizer().fit(docs)
    vectors = vectorizer.transform(docs)

    role_vectors = vectors[:-1]
    resume_vector = vectors[-1]

    sims = cosine_similarity(role_vectors, resume_vector.reshape(1, -1)).ravel()
    idx = sims.argsort()[::-1][:top_k]

    return [(roles[i], float(sims[i])) for i in idx]
