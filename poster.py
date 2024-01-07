
    
import streamlit as st
import requests
import pickle


def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US'.format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
    return full_path


movie = pickle.load(open('movie_list.pkl', 'rb'))
sim = pickle.load(open('sim.pkl', 'rb'))

movies_list = movie['title'].values

st.header('Movie Recommender')


selected_movie = st.selectbox('Select a movie:', movies_list)


if st.button('Show Recommendations'):
    
    index = movie[movie['title'] == selected_movie].index[0]
    distance = sorted(enumerate(sim.iloc[index]), reverse=True, key=lambda v: v[1])

    recommend_movie = []
    recommend_poster = []

    
    for i, dist in distance[1:6]:
        movie_id = movie.iloc[i].id
        recommend_movie.append(movie.iloc[i].title)
        recommend_poster.append(fetch_poster(movie_id))

    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommend_movie[0])
        st.image(recommend_poster[0])

    with col2:
        st.text(recommend_movie[1])
        st.image(recommend_poster[1])

    with col3:
        st.text(recommend_movie[2])
        st.image(recommend_poster[2])

    with col4:
        st.text(recommend_movie[3])
        st.image(recommend_poster[3])

    with col5:
        st.text(recommend_movie[4])
        st.image(recommend_poster[4])
