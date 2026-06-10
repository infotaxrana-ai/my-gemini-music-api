from flask import Flask, request, jsonify
import yt_dlp
import os

app = Flask(__name__)

def get_audio_stream_url(song_name):
    # ক্লাউড সার্ভারের জন্য সবচেয়ে নিরাপদ এবং লাইটওয়েট অপশনস
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'ignoreerrors': True,
        'source_address': '0.0.0.0', # নেটওয়ার্ক ব্লকিং এড়াতে
    }
    search_query = f"ytsearch1:{song_name}" # প্রথম রেজাল্টটি সরাসরি টার্গেট করার জন্য
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            if info and 'entries' in info and info['entries']:
                video_data = info['entries'][0]
                if video_data and 'url' in video_data:
                    return video_data['url']
    except Exception as e:
        print(f"Internal Fetch Error: {e}")
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
