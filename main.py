from flask import Flask, redirect, request

app = Flask(__name__)

# এই URL-টি সরাসরি ইউটিউবের অডিও স্ট্রিমে রিডাইরেক্ট করে
# এটি ইউটিউব সার্চ থেকে গান খুঁজে সরাসরি অডিও স্ট্রিমে পাঠিয়ে দিবে
@app.route('/get_audio', methods=['GET'])
def get_audio():
    track = request.args.get('track')
    # এটি সবচেয়ে স্টেবল পাবলিক এপিআই যা ইউটিউব অডিও স্ট্রিম দেয়
    return redirect(f"https://ytapi.xyz/stream?q={track}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
