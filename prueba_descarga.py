from pytube import YouTube

url = 'https://youtu.be/-y9OlfqNkvA'

try:
    yt = YouTube(url)
    stream = yt.streams.first()
    stream.download()
except Exception as e:
    print(f"An error occurred: {e}")
