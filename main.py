from flask import Flask, request
import requests
import re
import urllib.parse
import os

app = Flask(__name__)

def get_youtube_video_id(song_name):
    try:
        # সার্চ কুয়েরি ঠিক করা (স্পেস বা প্লাস যাই আসুক)
        clean_name = song_name.replace("+", " ").replace("%20", " ")
        formatted_query = urllib.parse.quote_plus(clean_name)
        search_url = f"https://www.youtube.com/results?search_query={formatted_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        video_ids = re.findall(r"\"videoId\":\"([^\"]+)\"", response.text)
        if video_ids:
            return video_ids[0]
    except Exception as e:
        print(f"Search Error: {e}")
    return None

def get_pure_audio_stream(video_id):
    # ইউটিউবের বট ব্লকিং বাইপাস করার জন্য একটি অত্যন্ত পাওয়ারফুল ও স্থায়ী ডাইরেক্ট এপিআই গেটওয়ে
    # এটি কোনো থার্ড-পার্টি পেজ বা ডাউনলোডার বাটন নয়, এটি সরাসরি পিওর অডিও ফাইলের লিংক দেয়
    gateway_url = f"https://api.v03.co/wp-json/api/v1/ytdl?url=https://www.youtube.com/watch?v={video_id}"
    
    try:
        res = requests.get(gateway_url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            # গেটওয়ে থেকে সরাসরি অডিও স্ট্রিম লিংকটি খুঁজে বের করা
            if 'links' in data and 'audio' in data['links']:
                return data['links']['audio']
    except Exception as e:
        print(f"Gateway Error: {e}")
        
    # ব্যাকআপ গেটওয়ে (যদি প্রথমটি কখনো রেসপন্স না করে)
    return f"https://api.vevioz.com/api/button/mp3/{video_id}"

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    video_id = get_youtube_video_id(song_query)
    if video_id:
        direct_audio_link = get_pure_audio_stream(video_id)
        if direct_audio_link:
            # সরাসরি ক্লিন টেক্সট আকারে আসল ডাইরেক্ট অডিও লিংকটি পাঠাবে
            return direct_audio_link, 200
            
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
