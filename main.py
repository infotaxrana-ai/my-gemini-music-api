from flask import Flask, redirect, request

app = Flask(__name__)

@app.route('/get_audio', methods=['GET'])
def get_audio():
    track = request.args.get('track', 'tahsan')
    # ইউটিউবের সরাসরি এম্বেড লিঙ্ক ব্যবহার করুন
    # এটি কোনো কনভার্টার নয়, এটি ইউটিউবের অফিসিয়াল প্লেয়ার লিঙ্ক
    return redirect(f"https://www.youtube.com/embed?autoplay=1&listType=search&list={track}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
