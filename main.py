from flask import Flask, request
import requests
import re
import urllib.parse
import os

app = Flask(__name__)

def get_esp_direct_audio_url(song_name):
    try:
        # ১. স্পেসগুলোকে প্লাস (+) চিহ্নে রূপান্তর করে ইউটিউবে সার্চ করা
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
            
            # ২. একটি গ্লোবাল ওপেন-সোর্স অডিও গেটওয়ে (Invidious Instance) ব্যবহার করা
            # এটি কোনো রিডাইরেক্ট বা বিজ্ঞপ্তির ঝামেলা ছাড়াই সরাসরি অডিও ডেটা স্ট্রিম করে, যা ESP-র জন্য বেস্ট।
            audio_api_url = f"https://invidious.nerdvpn.de/api/v1/videos/{video_id}"
            
            api_response = requests.get(audio_api_url, timeout=10)
            data = api_response.json()
            
            # ৩. শুধু অডিও ফরম্যাটের ডাইরেক্ট লিংকগুলো খুঁজে বের করা
            if 'adaptiveFormats' in data:
                for fmt in data['adaptiveFormats']:
                    # টাইপ যদি অডিও হয় (যেমন: audio/webm বা audio/mp4)
                    if 'audio/' in fmt.get('type', ''):
                        direct_url = fmt.get('url')
                        if direct_url:
                            return direct_url
                            
    except Exception as e:
        print(f"ESP Friendly API Error: {e}")
        return None
    return None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    # সরাসরি পিওর টেক্সট আকারে ডাইরেক্ট অডিও লিংক রিটার্ন করবে
    direct_audio_link = get_esp_direct_audio_url(song_query)
    if direct_audio_link:
        return direct_audio_link, 200
        
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
