import json
from spotify_api_handler import SpotifyAPIHandler

def get_artist_info(artist_name):
    data = SpotifyAPIHandler().search_for_artist(artist_name)
    if data:
        artist_items = data.get("artists", {}).get("items", [])
        if artist_items:
            artist = artist_items[0]
            images = artist.get('images', [])  # Get the images array
            image_url = images[0]['url'] if images else None  # Get the first image URL if available
            return {
                'name': str(artist.get('name', 'Unknown')),
                'followers': int(artist.get('followers', {}).get('total', 0)),
                'genres': artist.get('genres', []),
                'popularity': int(artist.get('popularity', 0)),
                'image': image_url,  # Add the image URL to the response
                'id': str(artist.get('id', 'Unknown'))
            }
    return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        artist_name = sys.argv[1]  # Get the artist name from the command-line argument
        artist_info = get_artist_info(artist_name)
        if artist_info:
            # Write the artist info dictionary to a JSON file
            with open("./apis/artist_info.json", "w") as json_file:
                json.dump(artist_info, json_file, indent=4)  # Pretty-print the JSON
            print(f"Artist information saved to artist_info.json")
        else:
            error_data = {"error": f"No information found for {artist_name}"}
            with open("artist_info.json", "w") as json_file:
                json.dump(error_data, json_file, indent=4)  # Save the error message to the JSON file
            print(f"No information found for {artist_name}. Error saved to artist_info.json")