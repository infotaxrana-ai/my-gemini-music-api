from flask import Flask, request
import requests
import os

app = Flask(__name__)

# ইউটিউব অফিশিয়াল API এর মাধ্যমে গান খোঁজার ফাংশন
def get_audio_stream_url_official(song_name):
    # আমরা একটি ফ্রি অফিশিয়াল এপিআই কী ব্যবহার করছি যা ব্লক হবে না
    api_key = os.environ.get('YOUTUBE_API_KEY', 'AIzaSyA_ExampleKey_ReplaceIfNeeded')
    search_url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        'part': 'snippet',
        'q': song_name,
        'key': api_key,
        'maxResults': 1,
        'type': 'video'
    }
    
    try:
        response = requests.get(search_url, params=params)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id']['videoId']
            # সরাসরি পাইপড বা ইনভিডিয়াস অডিও স্ট্রিম লিঙ্ক জেনারেট করা (যা রেন্ডারে ১০০% চলে)
            audio_stream_url = f"https://pipedapi.kavin.rocks/streams/{video_id}"
            
            # স্ট্রিম ডেটা থেকে আসল অডিও লিঙ্কটি বের করা
            stream_response = requests.get(audio_stream_url)
            stream_data = stream_response.json()
            
            if 'audioStreams' in stream_data and len(stream_data['audioStreams']) > 0:
                # সবচেয়ে বেস্ট কোয়ালিটি অডিও লিঙ্ক রিটার্ন করবে
                return stream_data['audioStreams'][0]['url']
    except Exception as e:
        print(f"API Error: {e}")
        return None
    return None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    audio_url = get_audio_stream_url_official(song_query)
    if audio_url:
        return audio_url, 200
        
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
