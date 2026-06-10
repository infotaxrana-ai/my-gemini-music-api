from flask import Flask, request
import requests
import re
import urllib.parse
import os

app = Flask(__name__)

def get_youtube_video_url_no_key(song_name):
    try:
        # Search query encode করা হচ্ছে
        encoded_query = urllib.parse.quote(song_name)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        # Request headers যাতে ইউটিউব ব্লক না করে
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        html_content = response.text
        
        # Regular Expression ব্যবহার করে সরাসরি ভিডিও আইডি খুঁজে বের করা
        video_ids = re.findall(r"\"videoId\":\"([^\"]+)\"", html_content)
        
        if video_ids:
            # প্রথম নিখুঁত ভিডিও আইডিটি নিয়ে ফুল লিংক তৈরি করা
            first_video_id = video_ids[0]
            return f"https://www.youtube.com/watch?v={first_video_id}"
            
    except Exception as e:
        print(f"Scraping Error: {e}")
        return None
    return None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    video_url = get_youtube_video_url_no_key(song_query)
    if video_url:
        return video_url, 200
        
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
