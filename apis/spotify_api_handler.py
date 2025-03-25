#!/usr/bin/env python3

from dotenv import load_dotenv
import os
from requests import get
from requests import post
import json
import base64

class SpotifyAPIHandler:
    def __init__(self):
        load_dotenv()

        self.CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        self.AUTH_URL = "https://accounts.spotify.com/api/token"
        #Save the access token
        self.get_token()

        #Need to pass access token into header to send properly formed GET request to API server
        self.headers = {
            'Authorization': 'Bearer {token}'.format(token=self.access_token)
        }
        self.BASE_URL = 'https://api.spotify.com/v1/'

    def get_token(self):
        auth_string = f"{self.CLIENT_ID}:{self.CLIENT_SECRET}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = str(base64.b64encode(auth_bytes).decode('utf-8'))

        self.AUTH_URL = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "client_credentials"
        }
        result = post(self.AUTH_URL, headers=headers, data=data)
        json_result = json.loads(result.content)
        self.access_token = json_result['access_token']

    def get_auth_header(self, token):
        return {
            'Authorization': f'Bearer {token}'
        }

    def search_for_artist(self, artist_name):
        url = "https://api.spotify.com/v1/search"
        headers = self.get_auth_header(self.access_token)
        query = f"?q={artist_name}&type=artist&limit=1"

        query_url = url + query
        result = get(query_url, headers=headers)
        json_result = json.loads(result.content)
        # Print the JSON data by key and value
        if result.status_code != 200:
            print(f"Error: {json_result.get('error', {}).get('message', 'Unknown error')}")
            return None
        return json_result
    
    def get_id(self, artist_name):
        data = self.search_for_artist(artist_name)
        if data:
            artist_items = data.get("artists", {}).get("items", [])
            if artist_items:
                artist = artist_items[0]
                return artist.get('id', 'Unknown')
        return None
    
    def _get_top_tracks(self, artist_name):
        artist_id = self.get_id(artist_name)
        headers = self.get_auth_header(self.access_token)
        if artist_id:
            url = f"{self.BASE_URL}artists/{artist_id}/top-tracks?country=US"
            result = get(url, headers=headers)
            json_result = json.loads(result.content)
            if result.status_code != 200:
                print(f"Error: {json_result.get('error', {}).get('message', 'Unknown error')}")
                return None
            return json_result
        return None

# if __name__ == "__main__":
#     spotify_api_handler = SpotifyAPIHandler()
#     print(spotify_api_handler.search_for_artist("Ado")) # JSON testing