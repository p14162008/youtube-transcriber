from pytubefix import YouTube

def download_youtube_video(url, output_path="video.mp4"):
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()
    stream.download(filename=output_path)
    return output_path
