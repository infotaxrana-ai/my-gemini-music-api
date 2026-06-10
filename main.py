from flask import Flask, redirect, request
import requests
import re
import os

app = Flask(__name__)

def get_video_id(song_name):
    # আপনার আগের আইডি খোঁজার লজিকটি সঠিক আছে
    query = song_name.replace(" ", "+")
    search_url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(search_url, timeout=10)
    video_ids = re.findall(r"\"videoId\":\"([^\"]+)\"", response.text)
    return video_ids[0] if video_ids else None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    video_id = get_video_id(song_query)
    if video_id:
        # মেইন পরিবর্তন এখানে: আমরা সরাসরি রিডাইরেক্ট করে দিচ্ছি 
        # সরাসরি অডিও স্ট্রিম লিঙ্কে (Piped API ব্যবহার করে)
        return redirect(f"https://piped.video/videoplayback?id={video_id}")
        
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
