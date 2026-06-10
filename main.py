from flask import Flask, request
import requests
import re
import urllib.parse
import os

app = Flask(__name__)

def get_youtube_video_url_perfect(song_name):
    try:
        # এখানে স্পেস বা যেকোনো ক্যারেক্টারকে একদম ইউটিউবের মতো প্লাস (+) চিহ্নে রূপান্তর করা হচ্ছে
        formatted_query = song_name.replace(" ", "+")
        encoded_query = urllib.parse.quote_plus(formatted_query)
        
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        html_content = response.text
        
        # ইউটিউবের পেজ সোর্স থেকে ভিডিও আইডি খোঁজার সবচেয়ে শক্তিশালী মেথড
        video_ids = re.findall(r"\"videoId\":\"([^\"]+)\"", html_content)
        
        if video_ids:
            # প্রথম সঠিক ভিডিও আইডিটি নিয়ে লিংক তৈরি
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
            
    except Exception as e:
        print(f"Error: {e}")
        return None
    return None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    video_url = get_youtube_video_url_perfect(song_query)
    if video_url:
        return video_url, 200
        
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
