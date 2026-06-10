from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    track = request.args.get('track')
    # পিওর অডিও স্ট্রিম লিঙ্ক পাওয়ার জন্য Piped API
    # এই লিঙ্কটি সরাসরি অডিও ফাইল দেয়, কোনো ডাউনলোড বাটন নয়
    search_url = f"https://piped-api.kavin.rocks/search?q={track}&filter=videos"
    
    try:
        res = requests.get(search_url, timeout=5).json()
        if res['items']:
            video_id = res['items'][0]['url'].split('v=')[-1]
            # অডিও স্ট্রিম লিঙ্ক
            return f"https://piped-api.kavin.rocks/streams/{video_id}"
    except:
        return "Error"
    return "Error"
