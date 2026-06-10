from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Official YouTube API Key
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', 'AIzaSyDhO1_N_f-86mD9_YV70kG2j8Xl102Am4c')

def get_youtube_video_url(song_name):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': song_name,
        'key': YOUTUBE_API_KEY,
        'maxResults': 1,
        'type': 'video'
    }
    
    try:
        response = requests.get(search_url, params=params)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id']['videoId']
            # Returns official YouTube video link
            return f"https://www.youtube.com/watch?v={video_id}"
    except Exception as e:
        print(f"API Error: {e}")
        return None
    return None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    video_url = get_youtube_video_url(song_query)
    if video_url:
        return video_url, 200
        
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
