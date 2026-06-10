from flask import Flask, request
import requests
import re
import urllib.parse
import os

app = Flask(__name__)

def get_pure_esp_audio_url(song_name):
    try:
        # ১. সার্চ কুয়েরি ইউটিউব স্টাইলে প্লাস চিহ্নে রূপান্তর
        formatted_query = song_name.replace(" ", "+")
        encoded_query = urllib.parse.quote_plus(formatted_query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        video_ids = re.findall(r"\"videoId\":\"([^\"]+)\"", response.text)
        
        if video_ids:
            video_id = video_ids[0]
            
            # ২. একটি অত্যন্ত স্টেবল ও গ্লোবাল ওপেন-সোর্স অডিও প্রোভাইডার মেকানিজম ব্যবহার করা
            # এটি সরাসরি র (Raw) অডিও ফাইল স্ট্রিম লিঙ্ক জেনারেট করে যা কোনো হোস্টিংয়ে ব্লক হয় না
            direct_provider_url = f"https://api.cobalt.tools/api/json"
            
            payload = {
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "downloadMode": "audio",
                "audioFormat": "mp3",
                "audioBitrate": "128"
            }
            
            api_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            api_response = requests.post(direct_provider_url, json=payload, headers=api_headers, timeout=10)
            
            if api_response.status_code == 200:
                data = api_response.json()
                if 'url' in data:
                    # সরাসরি ডাইরেক্ট অডিও .mp3 ফাইল লিঙ্কটি রিটার্ন করবে
                    return data['url']
                    
    except Exception as e:
        print(f"ESP Configuration Error: {e}")
        return None
    return None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    # সরাসরি পিওর টেক্সট আকারে ক্লিন ও র অডিও ফাইলের লিঙ্ক রিটার্ন করবে
    direct_audio_link = get_pure_esp_audio_url(song_query)
    if direct_audio_link:
        return direct_audio_link, 200
        
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
