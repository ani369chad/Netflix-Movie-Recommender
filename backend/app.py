import pandas as pd
import numpy as np
import faiss
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset
df = pd.read_csv("netflix_titles.csv").fillna("")

# Load FAISS index
index = faiss.read_index("index")

# Function: convert row into a string
def create_textual_representation(row):
    return f"""
    Type: {row['type']}, 
    Title: {row['title']}, 
    Director: {row['director']}, 
    Cast: {row['cast']}, 
    Released: {row['release_year']},
    Genre: {row['listed_in']},
    Description: {row['description']}"""

@app.get("/recommend")
def recommend(movie_id: int = Query(..., description="Row index of favorite movie")):
    # Pick the movie row
    favorite_movie = df.iloc[movie_id]

    # Get embedding from Ollama
    res = requests.post("http://localhost:11434/api/embeddings",
                        json={"model": "llama2",
                              "prompt": create_textual_representation(favorite_movie)})
    
    embedding = np.array([res.json()['embedding']], dtype='float32')

    # Search FAISS index
    D, I = index.search(embedding, 6)

    # Collect results
    results = []
    for idx in I[0]:
        row = df.iloc[idx]
        results.append({
            "title": row["title"],
            "type": row["type"],
            "year": int(row["release_year"]),
            "genre": row["listed_in"],
            "description": row["description"]
        })
    return {"recommendations": results}
