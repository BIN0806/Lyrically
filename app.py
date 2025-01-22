import pickle
import streamlit as st
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()
#You will need to supplement your own client_id and secret_id from the spotify developer website
CLIENT_ID = os.getenv("CLIENT_ID")
SECRET_ID = os.getenv("SECRET_ID")



# Initializing Spotify Client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=SECRET_ID)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    result = sp.search(q=search_query, type="track")
    
    if result and result["tracks"]["items"]:
        track = result["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"
    
def recommend(song):
    i = music[music['song'] == song].index[0]
    distance = sorted(list(enumerate(similarity[i])), reverse=True, key=lambda x: x)
    recommended_music_names = []
    recommended_music_posters = []
    for i in distance[1:6]:
        # Fetch the movie poster
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
    return recommended_music_names,recommended_music_posters

st.header('Music Recommender System')
music = pickle.load(open('ds.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

music_list = music['song'].values
selected_music = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)
if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_music)
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])
    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])