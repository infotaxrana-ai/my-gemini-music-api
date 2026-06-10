from flask import Flask, redirect

app = Flask(__name__)

@app.route('/get_audio')
def get_audio():
    # এটি একটি পাবলিক মিউজিক রেডিও স্ট্রিম, এটি পিসি এবং ইএসপি দুটিতেই চলবে
    return redirect("http://icecast.radiofrance.fr/fip-midfi.mp3")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
