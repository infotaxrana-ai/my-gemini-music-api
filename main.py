from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    # সরাসরি অডিও ফাইল স্ট্রিম করার লিঙ্ক
    return redirect("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
