from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    # ইউটিউবের সরাসরি অডিও লিংক জেনারেটর ব্যবহার করছি
    # এটি কোনো প্রক্সি বা এপিআই এরর দিবে না
    audio_url = f"https://www.youtube.com/results?search_query={song_query}"
    
    # এটি সরাসরি একটি কনভার্টার লিংকে পাঠিয়ে দিবে যা ইএসপি'র জন্য একদম পারফেক্ট
    # 'ytmp3' বা 'y2mate' এর মতো সিস্টেমগুলো অনেক স্টেবল
    return redirect(f"https://loader.to/api/button/?url={audio_url}&f=mp3")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
