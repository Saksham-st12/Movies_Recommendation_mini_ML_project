import streamlit as st
import pickle
import requests
import os
import gdown


OMDB_API_KEY = st.secrets.get("OMDB_API_KEY", "")
if not OMDB_API_KEY:
    st.warning("OMDb API key not found! Please add it in Streamlit secrets.")



@st.cache_data(show_spinner=False)
def load_similarity():
    SIMILARITY_FILE = "similarity.pkl"
    if not os.path.exists(SIMILARITY_FILE):
        url = "https://drive.google.com/uc?id=1-9e1P3WudLv3dpXP9UmGMZO99C2hLiF_"
        gdown.download(url, SIMILARITY_FILE, quiet=False)
    return pickle.load(open(SIMILARITY_FILE, "rb"))



movies_df = pickle.load(open("movies.pkl", "rb"))
similarity = load_similarity()



@st.cache_data(show_spinner=False)
def fetch_poster(title):
    if not OMDB_API_KEY:
        return "https://via.placeholder.com/500x750?text=No+API+Key"

    url = f"http://www.omdbapi.com/?t={requests.utils.quote(title)}&apikey={OMDB_API_KEY}"
    try:
        data = requests.get(url, timeout=5).json()
        poster = data.get("Poster")
        if poster and poster != "N/A":
            return poster
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.Timeout:
        return "https://via.placeholder.com/500x750?text=Timeout"
    except Exception:
        return "https://via.placeholder.com/500x750?text=Error+Loading"


@st.cache_data(show_spinner=False)
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



st.title(" Movie Recommender System")

movie_titles = movies_df['Title'].values
option = st.selectbox("Which movie do you like?", movie_titles)

if st.button("Recommend"):
    with st.spinner("Finding recommendations..."):
        recommendations, posters = recommend(option)
    cols = st.columns(len(recommendations))
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_column_width=True)
            st.caption(recommendations[idx])
