# Movie Recommender System (Content-Based ML + Streamlit Deployment)

## Project Overview
This project is a **content-based movie recommender system** that suggests similar movies based on plot, genre, keywords, cast, and director information.  
It uses **Natural Language Processing (NLP)** to understand movie similarity and is deployed as an interactive **Streamlit web app**.  
Users can select a movie from the dropdown and instantly get five similar movie recommendations with posters.

---

## Machine Learning Workflow (from main.ipynb)

### 1. Data Loading and Preparation
- Datasets used:
  - `tmdb_5000_movies.csv`
  - `tmdb_5000_credits.csv`
- Both files were merged on the `id` column to form a single DataFrame.
- Unnecessary columns like budget, language, and homepage were dropped.
- Key columns used: `['id', 'Title', 'genres', 'keywords', 'overview', 'cast', 'crew']`.

### 2. Data Cleaning and Transformation
- Converted JSON-like string columns (`genres`, `keywords`, `cast`, `crew`) into Python lists using `ast.literal_eval`.
- Extracted top 3 cast members and the director’s name.
- Removed spaces and normalized text using underscores (e.g., `Science Fiction` → `Science_Fiction`).
- Tokenized movie overviews into words.

### 3. Tag Generation
- Combined multiple features (`overview`, `genres`, `keywords`, `cast`, `Director`) into a single column called `tags`.
- Example:
tags = overview + genres + keywords + cast + Director
- - Transformed all tags into lowercase for uniformity.

### 4. Text Preprocessing
- Applied **stemming** using `PorterStemmer` to reduce words to their root form (e.g., "loved", "loving" → "love").

### 5. Feature Extraction
- Converted text data into numerical vectors using **CountVectorizer** (Bag of Words model).
- Limited vocabulary size to top 5000 words and removed English stopwords.

### 6. Similarity Calculation
- Used **Cosine Similarity** to compute pairwise similarity scores between movies.
- Stored the similarity matrix and processed movie data as:
- `movies.pkl` → metadata (movie titles, tags)
- `similarity.pkl` → cosine similarity matrix

---

## Streamlit Web Application

### App Functionality
1. Select a movie from the dropdown.
2. Click **"Recommend"** to get 5 similar movies.
3. View recommendations with posters fetched using the **OMDb API**.

### Key Features
- OMDb API integration (India-friendly alternative to TMDB).
- Uses `st.cache_data` for faster response times and reduced API calls.
- Streamlit columns layout to display movie posters side-by-side.
- Clean and responsive user interface.

---

## Technologies Used

| Category | Tools/Libraries |
|-----------|----------------|
| **Language** | Python |
| **Data Handling** | Pandas, NumPy |
| **NLP / ML** | Scikit-learn, NLTK |
| **Web App** | Streamlit |
| **API Integration** | OMDb API |
| **Storage** | Pickle |

---

## Streamlit Link 
-https://moviesrecommendationminimlproject-sm2envbupdmmb8xv2wvmzg.streamlit.app/
