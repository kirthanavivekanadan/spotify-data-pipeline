import json
import requests
import boto3
from datetime import datetime

def lambda_handler(event, context):

    # Spotify API credentials
    CLIENT_ID = ''  # Replace with your actual client ID
    CLIENT_SECRET = ''  # Replace with your actual client secret
    REDIRECT_URI = 'http://localhost:8888/callback'

    # Get access token
    auth_response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'client_credentials'
    }, auth=(CLIENT_ID, CLIENT_SECRET))
    auth_data = auth_response.json()
    access_token = auth_data['access_token']

    # Fetch playlist data (add the playlist ID here)
    playlist_id = '5v079teeUpj6mCB6lQn042'  # Replace with your actual playlist ID
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    playlist_response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=headers)

    # Check if the request was successful
    if playlist_response.status_code != 200:
        print(f"Error fetching playlist data: {playlist_response.status_code}")
        print(playlist_response.text)  # Log the error message
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error fetching playlist data: {playlist_response.text}")
        }

    playlist_data = playlist_response.json()

    # Check if the API response contains an error
    if 'error' in playlist_data:
        print(f"Error from Spotify API: {playlist_data['error']}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error from Spotify API: {playlist_data['error']}")
        }

    # Safely access 'items' in the playlist response
    items = playlist_data.get('items', [])
    if not items:
        print("No items found in the playlist.")
        return {
            'statusCode': 500,
            'body': json.dumps('No items found in the playlist.')
        }

    # Prepare data for S3 - Filter tracks by Arijit Singh
    arijit_tracks = []
    for item in items:
        track = item['track']
        # Check if the artist is Arijit Singh
        if any(artist['name'] == 'Arijit Singh' for artist in track['artists']):
            arijit_tracks.append({
                'track_id': track['id'],
                'track_name': track['name'],
                'artist_name': track['artists'][0]['name'],
                'album_name': track['album']['name'],
                'release_date': track['album']['release_date']
            })

    # Check if we found any Arijit Singh songs
    if not arijit_tracks:
        print("No Arijit Singh tracks found in the playlist.")
        return {
            'statusCode': 500,
            'body': json.dumps('No Arijit Singh tracks found in the playlist.')
        }


# Upload to S
    s3 = boto3.client('s3')
    bucket_name = 'spotify-data-pipeline-kirthi'  # Replace with your S3 bucket name
    file_name = f'spotify_tracks_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=json.dumps(arijit_tracks))

    return {
    'statusCode': 200,
    'body': json.dumps('Data uploaded to S3 successfully')
    }
