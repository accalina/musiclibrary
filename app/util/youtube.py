
import os
import youtube_dl
import socketio

io = socketio.Client()

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

def download_mp3(url):
    io.connect('http://localhost:5000')

    io.emit("message",f"Downloading... (eta 5min)")
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    io.emit("message","Saving file")
    for file in os.listdir():
        if file.endswith(".mp3"):
            os.system(f"mv '{file}' static/music/")
    io.emit("message","Done!")

# def extract_info():
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         result = ydl.extract_info(
#             'https://www.youtube.com/watch?v=EWKX3wass9s',
#             download=False
#         )
#     # print(result)
#     if 'entries' in result:
#         # Can be a playlist or a list of videos
#         video = result['entries'][0]
#     else:
#         # Just a video
#         video = result

#     print(video)
#     video_url = video['url']
#     print(video_url)

# if __name__ == "__main__":
#     extract_info()