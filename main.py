from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    # এখানে track-এ গানের নাম বা ইউটিউব ভিডিও আইডি দিন
    track = request.args.get('track', 'tahsan')
    
    # Piped API এর মাধ্যমে সরাসরি অডিও স্ট্রিম লিঙ্ক রিডাইরেক্ট হবে
    # এটি সবচেয়ে বেশি স্টেবল এবং পিসি/ইএসপি দুটিতেই চলবে
    return redirect(f"https://piped.video/watch?v={track}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
