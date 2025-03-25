import sys
from spotify_api_handler import SpotifyAPIHandler

def get_followers(artist_name):
    data = SpotifyAPIHandler().search_for_artist(artist_name)
    if data:
        artist_items = data.get("artists", {}).get("items", [])
        if artist_items:
            artist = artist_items[0]
            return artist.get('followers', []).get('total', 0)
    return None

def get_name(artist_name):
    data = SpotifyAPIHandler().search_for_artist(artist_name)
    if data:
        artist_items = data.get("artists", {}).get("items", [])
        if artist_items:
            artist = artist_items[0]
            return artist.get('name', [])
    return None

if __name__ == "__main__":
     if len(sys.argv) > 1:
        artist_name = sys.argv[1]  # Get the artist name from the command-line argument
        followers = get_followers(artist_name)
        name = get_name(artist_name)
        if followers is not None:
            format_followers = f"{followers:,}"
        print(f"Spotify Artist \'{name}\' has {format_followers} followers.")