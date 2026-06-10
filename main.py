from flask import Flask, redirect

app = Flask(__name__)

# আপনার ইউটিউব ভিডিও আইডি টি এখানে পাঠাবেন
@app.route('/stream/<video_id>')
def stream_audio(video_id):
    # Piped API এর মাধ্যমে অডিও স্ট্রিম করা সবচেয়ে নিরাপদ
    return redirect(f"https://piped.video/videoplayback?id={video_id}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
