import sys
import json
import os
from spotify_api_handler import SpotifyAPIHandler

def get_top_tracks(artist_name):
    data = SpotifyAPIHandler()._get_top_tracks(artist_name)
    if data:
        return data.get("tracks", [])

def get_track_names(tracks):
    return [track.get('name', 'Unknown') for track in tracks]

def get_album_names(tracks):
    return [track.get('album', {}).get('name', 'Unknown') for track in tracks]

def get_popularity(tracks):
    return [track.get('popularity', 0) for track in tracks]

def get_track_numbers(tracks):
    return [track.get('track_number', 0) for track in tracks]

def get_release_dates(tracks):
    return [track.get('album', {}).get('release_date', 'Unknown') for track in tracks]

def get_image_urls(tracks):
    return [track.get('album', {}).get('images', [{}])[0].get('url', 'Unknown') for track in tracks]

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
        top_tracks = get_top_tracks(artist_name)
        name = get_name(artist_name)
        image_urls = get_image_urls(top_tracks)
        if top_tracks is not None:
            track_names = get_track_names(top_tracks)
            album_names = get_album_names(top_tracks)
            popularity = get_popularity(top_tracks)
            track_numbers = get_track_numbers(top_tracks)
            release_dates = get_release_dates(top_tracks)
            # Write the images dictionary to a JSON file
            for i, track in enumerate(track_names):
                print(f"{i + 1}. {track}\n\tAlbum: {album_names[i]}\n\tPopularity: {popularity[i]}\n\tTrack Number: {track_numbers[i]}\n\tRelease Date: {release_dates[i]}\n")
            
        else:
            print(f"No top tracks found for artist '{artist_name}'.")
        
        # Ensure the file is overwritten
        output_file = os.path.join(os.path.dirname(__file__), "top_track_imgs.json")
        if image_urls:
            with open(output_file, "w") as json_file:
                print(f"Overwriting {output_file} with new data.")
                json.dump(image_urls, json_file, indent=4)
        else:
            print("No valid image URLs found. Skipping file update.")
