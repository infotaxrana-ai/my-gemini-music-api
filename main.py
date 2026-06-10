from flask import Flask, request
import yt_dlp
import os

app = Flask(__name__)

def get_audio_stream_url(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'nocheckcertificate': True,
        'ext': 'mp3',
    }
    search_query = f"ytsearch:{song_name}"
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(search_query, download=False)
            if 'entries' in info and len(info['entries']) > 0:
                return info['entries'][0]['url']
        except Exception as e:
            print(f"Error: {e}")
            return None
    return None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    audio_url = get_audio_stream_url(song_query)
    if audio_url:
        return audio_url, 200
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
