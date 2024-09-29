import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f64b54a96e891fe5fda86c7cb18f1a06".format(movie_id)
    data = requests.get(url)
    data = data.json()

    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:11]:  # Get 10 recommendations (1:11 to skip the selected movie)
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')
movies = pickle.load(open('./models/movie_list.pkl', 'rb'))
similarity = pickle.load(open('./models/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create two rows of five columns each
    for i in range(0, 10, 5):  # Loop in steps of 5 for each row
        cols = st.columns(5)  # Create 5 columns
        for j in range(5):  # Loop through 5 items
            if i + j < len(recommended_movie_names):  # Check to avoid index out of range
                with cols[j]:
                    st.text(recommended_movie_names[i + j])
                    st.image(recommended_movie_posters[i + j])

