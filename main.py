from flask import Flask, request, redirect
import requests

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    # এটি ইউটিউব থেকে গানটি খুঁজে বের করে সরাসরি অডিও লিংকে পাঠিয়ে দেবে
    # cobalt.tools হলো ইউটিউবের অডিও সরাসরি পাওয়ার সবথেকে বিশ্বস্ত উপায়
    api_url = "https://api.cobalt.tools/api/json"
    payload = {
        "url": f"https://www.youtube.com/results?search_query={song_query}",
        "downloadMode": "audio",
        "audioFormat": "mp3"
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, json=payload, headers=headers).json()
        if 'url' in response:
            return response['url'] # সরাসরি অডিও ফাইলের লিংক
    except:
        return "ERROR: Failed", 500
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
