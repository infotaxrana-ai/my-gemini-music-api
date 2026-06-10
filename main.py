from flask import Flask, request
import yt_dlp
import os

app = Flask(__name__)

def get_youtube_pure_audio(song_name):
    # ইউটিউবের অফিশিয়াল সার্ভার থেকে সরাসরি পিওর অডিও সোর্স ইউআরএল বের করার বেস্ট কনফিগারেশন
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'source_address': '0.0.0.0',
        'skip_download': True,
    }
    
    # স্পেস বা প্লাস যাই আসুক, ইউটিউব সার্চ কুয়েরি ঠিক করে নেবে
    clean_query = song_name.replace("+", " ")
    search_query = f"ytsearch1:{clean_query}"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            if info and 'entries' in info and info['entries']:
                video_data = info['entries'][0]
                # সরাসরি অফিশিয়াল গুগলের অডিও স্ট্রিম ইউআরএল (googlevideo.com/videoplayback...)
                if 'url' in video_data:
                    return video_data['url']
    except Exception as e:
        print(f"Extraction Error: {e}")
        return None
    return None

@app.route('/get_audio', methods=['GET'])
def get_audio():
    song_query = request.args.get('track')
    if not song_query:
        return "ERROR: No track name", 400
    
    direct_audio_url = get_youtube_pure_audio(song_query)
    if direct_audio_url:
        return direct_audio_url, 200
        
    return "ERROR: Not Found", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
