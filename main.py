from pytube import YouTube

# URL del video que deseas descargar
video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

# Crear objeto YouTube
yt = YouTube(video_url)

# Obtener el stream de video de mayor resolución
video_stream = yt.streams.get_highest_resolution()

# Descargar el video en el directorio actual
video_stream.download()

print(f"Video '{yt.title}' descargado exitosamente!")
