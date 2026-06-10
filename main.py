from flask import Flask, redirect, request
import requests

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    track = request.args.get('track')
    # ইউটিউবের সরাসরি সার্চ পেজে রিডাইরেক্ট করা হচ্ছে
    # এটি কোনো থার্ড পার্টি সাইটে যাবে না
    return redirect(f"https://www.youtube.com/results?search_query={track}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
