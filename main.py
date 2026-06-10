from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# ESP-র জন্য ডাইরেক্ট এবং স্থায়ী অডিও ফাইলের সোর্স ডিকশনারি
# (এখানে ড্রপবক্স বা আপনার নিজস্ব স্টোরেজের ডাইরেক্ট .mp3 লিঙ্ক বসানো, যা কখনো ব্লক হবে না)
AUDIO_DATABASE = {
    "kishore+kumar+song": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", # টেস্ট করার জন্য একটি পাবলিক mp3 লিঙ্ক
    "kishore kumar song": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "ayman serhani": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "habibi song": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
}

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    # ছোট হাতের অক্ষরে কনভার্ট করে সার্চ ম্যাচ করা হচ্ছে
    clean_query = song_query.lower().strip()
    
    # আমাদের ডাটাবেজে গানটি থাকলে সরাসরি তার পিওর ডাইরেক্ট .mp3 লিঙ্কটি টেক্সট আকারে রিটার্ন করবে
    if clean_query in AUDIO_DATABASE:
        return AUDIO_DATABASE[clean_query], 200
    
    # যদি নির্দিষ্ট কোনো গান না মেলে, তবে টেস্ট করার সুবিধার জন্য প্রথম ডিফল্ট গানটির লিঙ্কই রিটার্ন করবে
    return AUDIO_DATABASE["kishore kumar song"], 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
