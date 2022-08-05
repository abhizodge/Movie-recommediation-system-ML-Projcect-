import streamlit as st
import pandas as pd
import pickle
import requests

movies = pd.read_pickle('movie_dict .pkl')
similarity = pickle.load(open('similarity.pkl', 'rb'))


def recommend(title):
    rec_movies = []
    poster_paths = []

    movie_index = movies[movies['title'] == title].index[0]
    sorted_index = sorted(list(enumerate(similarity[movie_index])), reverse=True, key = lambda x: x[1])
    movie_index=movies.movie_id[movie_index]
    indices = sorted_index[1:6]

for index in indices:
        rec_movies.append(movies.title[index[0]])
        poster_paths.append(get_poster(movies.movie_id[index[0]]))
return rec_movies, poster_paths,movie_index

def get_trailer(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}//videos?api_key=ebed65049adc26c76bc712b0531ecdb5&language&language=en-US'.format(
        movie_id)
    response = requests.get(url)
    data = response.json()
return 'https://www.youtube.com/watch?v='+data['results'][0]['key']

def get_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=ebed65049adc26c76bc712b0531ecdb5&language=en-US'.format(movie_id)
    response = requests.get(url)
    data = response.json()
return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def get_details(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=ebed65049adc26c76bc712b0531ecdb5&language=en-US'.format(
        movie_id)
    response = requests.get(url)
    data = response.json()
    title = data['title']
    tagline = data['tagline']
    overview = data['overview']
    release = data['release_date']
    ratings = data['vote_average']
return title,tagline, overview, release, ratings

st.title('Movies for you')

selected = st.selectbox(
'Which Movie did you Watched ?',
movies['title'])

def show(selected_movie):
    names, posters, curr_pos = recommend(selected_movie)
    pos = get_poster(curr_pos)
    trailer = get_trailer(curr_pos)
    title, tagline, overview, rel_date, ratings = get_details(curr_pos)

    poster, detail = st.beta_columns(2)
    poster.image(pos)
    detail.header(title)
    detail.write(tagline)
    detail.write('Overview: ' + overview)
    detail.text('Release Date: ' + rel_date)
    detail.text('Ratings: {}'.format(ratings))
    detail.video(trailer)

    st.success('Recommended movies for you')

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.text(names[0])
    col1.image(posters[0])

    col2.text(names[1])
    col2.image(posters[1])

    col3.text(names[2])
    col3.image(posters[2])

    col4.text(names[3])
    col4.image(posters[3])

    col5.text(names[4])
    col5.image(posters[4])


if st.button('Recommend'):
    show(selected)

