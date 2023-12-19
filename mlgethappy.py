import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import sys

league_name = 'superfam-s3'
if len(sys.argv) > 1:
    league_name = sys.argv[1]

# Read Spotify API credentials from file
with open('spotify_credentials.txt', 'r') as file:
    lines = file.readlines()
    client_id = lines[0].split(':')[1].strip()
    client_secret = lines[1].split(':')[1].strip()

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load your CSV files
submissions_df = pd.read_csv(f'data/{league_name}/submissions.csv')
votes_df = pd.read_csv(f'data/{league_name}/votes.csv')

# Get all unique song URIs
uris = pd.concat([submissions_df['Spotify URI'], votes_df['Spotify URI']]).unique()

# Function to fetch track metadata and audio features
def get_track_info(uri_list):
    track_info = []

    for uri in uri_list:
        # Remove 'spotify:track:' from the URI
        track_id = uri.split(':')[-1]

        # Get track metadata
        track = sp.track(track_id)
        track_name = track['name']
        album_name = track['album']['name']
        artist_name = track['artists'][0]['name']
        popularity = track['popularity']

        # Get audio features
        features = sp.audio_features([track_id])[0]

        track_info.append({
            'Spotify URI': uri,
            'Track Name': track_name,
            'Artist Name': artist_name,
            'Album Name': album_name,
            'Popularity': popularity,
            'Danceability': features['danceability'],
            'Energy': features['energy'],
            'Key': features['key'],
            'Loudness': features['loudness'],
            'Mode': features['mode'],
            'Speechiness': features['speechiness'],
            'Acousticness': features['acousticness'],
            'Instrumentalness': features['instrumentalness'],
            'Liveness': features['liveness'],
            'Valence': features['valence'],
            'Tempo': features['tempo'],
            'Duration (ms)': features['duration_ms'],
            'Time Signature': features['time_signature']
        })
    
    return track_info

# Fetch the track info in batches of 50 (to avoid rate limits)
track_info = []
for i in range(0, len(uris), 50):
    track_info.extend(get_track_info(uris[i:i+50]))

# Create a dataframe with the track info
track_info_df = pd.DataFrame(track_info)

# Write the dataframe to a CSV file
track_info_df.to_csv(f'data/{league_name}/track_info.csv', index=False)