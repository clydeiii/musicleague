# https://open.spotify.com/playlist/2sbuHm71gCkDUyCwiEmAOl
import csv
import sys
from typing import DefaultDict
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


league_name = 'mazala-q4'
if len(sys.argv) > 1:
    league_name = sys.argv[1]

print(f"music league data for {league_name}")

rounds = []

with open(f"data/{league_name}/rounds.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rounds.append({'id': row['ID'], 'url': row['Playlist URL']})

