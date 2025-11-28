import os
import yt_dlp#Download a video transcript (using yt-dlp)
def download_transcript(video_url):
    print(f"Attempting download{video_url}")
    #Now we will configure yt-dlp to get only subtitles and not the video
    #Youtube-DL Options-->Python dictionary (a list of settings)
    ydl_opts={
        "skip_download":True,
        "writeautomaticsub":True,
        "writesub":True,
        "subtitleslangs":["en"],
        "outtmpl":"transcript_data",## Save as 'transcript_data
        "quiet":True
        }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            print("Downloaded successfully!!")
            return True
    except Exception as e:
        print(f"Error:{e}")
        return False
if (__name__)=="__main__":
    download_transcript("https://youtu.be/hn80mWvP-9g?si=m5r11FZmn5G9MR1E")

