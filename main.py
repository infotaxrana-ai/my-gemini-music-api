from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    track = request.args.get('track', 'kishore')
    # এটি ইউটিউব সার্চ থেকে পাওয়া প্রথম ভিডিওর সরাসরি অডিও লিঙ্ক দিবে
    return redirect(f"https://yt-stream.com/play?q={track}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
