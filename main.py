from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    track = request.args.get('track', 'tahsan')
    # এটি ইউটিউবের একটি পাবলিক অডিও গেটওয়ে
    # এটি সরাসরি অডিও ফাইলটি ইএসপি-র জন্য স্ট্রিম করবে
    return redirect(f"https://api.singlemusic.xyz/stream?q={track}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
