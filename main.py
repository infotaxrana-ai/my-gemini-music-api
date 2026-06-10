from flask import Flask, request
import yt_dlp
import os

app = Flask(__name__)

def get_audio_url_yt_dlp(song_name):
    # yt-dlp এর জন্য এমন কনফিগারেশন যা কোনো প্রকার কুকি বা সাইন-ইন ছাড়াই চলবে
    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'extract_flat': True,
        'force_generic_extractor': True, # এটি বট ডিটেকশন বাইপাস করতে সাহায্য করে
    }
    
    try:
        # সরাসরি ইউটিউব সার্চ করে প্রথম রেজাল্টটি নেবে
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_query = f"ytsearch1:{song_name}"
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' in info and info['entries']:
                video_url = info['entries'][0]['url']
                # এবার আসল অডিও স্ট্রিম ইউআরএলটি বের করা
                audio_info = ydl.extract_info(video_url, download=False)
                return audio_info['url']
                
    except Exception as e:
        print(f"yt-dlp Error: {e}")
        return None
    return None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    audio_link = get_audio_url_yt_dlp(song_query)
    if audio_link:
        return audio_link, 200
    return "ERROR: Could not fetch audio", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
