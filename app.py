import streamlit as st
import pickle
import requests


# Load pickled data
movies_df = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Load API key securely from Streamlit secrets
OMDB_API_KEY = st.secrets["OMDB_API_KEY"]

# Function to fetch poster using OMDb API
def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    try:
        data = requests.get(url, timeout=5).json()
        poster = data.get("Poster")
        if poster and poster != "N/A":
            return poster
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception:
        return "https://via.placeholder.com/500x750?text=Error+Loading"


# Function to recommend similar movies
def recommend(movie):
    movie_index = movies_df[movies_df['Title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        title = movies_df.iloc[i[0]].Title
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters


# Streamlit UI
st.title("Movie Recommender System")

movie_titles = movies_df['Title'].values
option = st.selectbox("Which movie do you like?", movie_titles)

if st.button("Recommend"):
    recommendations, posters = recommend(option)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx])
            st.caption(recommendations[idx])
