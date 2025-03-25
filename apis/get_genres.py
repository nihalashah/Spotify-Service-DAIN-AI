import sys
from spotify_api_handler import SpotifyAPIHandler

def get_genres(artist_name):
    data = SpotifyAPIHandler().search_for_artist(artist_name)
    if data:
        artist_items = data.get("artists", {}).get("items", [])
        if artist_items:
            artist = artist_items[0]
            genres = artist.get('genres', [])
            return [genre.capitalize() for genre in genres]
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
        genres = get_genres(artist_name)
        name = get_name(artist_name)
        if genres:
            print(f"Genres for {name}: {', '.join(genres)}")
        else:
            print(f"No genres found for {name}.")