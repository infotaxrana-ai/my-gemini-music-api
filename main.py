from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    try:
        # ১. Piped API ব্যবহার করে গান সার্চ করা (বট ডিটেকশন নেই)
        search_url = f"https://piped-api.kavin.rocks/search?q={song_query}&filter=videos"
        search_res = requests.get(search_url, timeout=10).json()
        
        if not search_res.get('items'):
            return "ERROR: Song not found", 404
            
        video_id = search_res['items'][0]['url'].split('/watch?v=')[-1]
        
        # ২. সরাসরি অডিও স্ট্রিম লিঙ্ক বের করা
        stream_url = f"https://piped-api.kavin.rocks/streams/{video_id}"
        stream_res = requests.get(stream_url, timeout=10).json()
        
        # ৩. সবথেকে ভালো কোয়ালিটির অডিও লিঙ্কটি রিটার্ন করা
        if 'audioStreams' in stream_res and stream_res['audioStreams']:
            audio_link = stream_res['audioStreams'][0]['url']
            return audio_link # ESP এই ডাইরেক্ট লিঙ্কটি রিড করবে
            
    except Exception as e:
        return f"ERROR: {str(e)}", 500
    
    return "ERROR: Could not fetch", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
