import flet as ft

def main(page: ft.Page):
    page.add(
        ft.ResponsiveRow(
            [
                ft.Container(
                    ft.TextField(label="YouTube URL/ID"),
                    padding=5,
                    col={"sm": 9, "md": 9, "xl": 9},
                ),
                ft.Container(
                    ft.FilledButton("Descargar...", icon="add"),
                    padding=5,
                    col={"sm": 3, "md": 3, "xl": 3},
                ),
            ],
        ),
        ft.ResponsiveRow(
            [
                ft.Container(
                    ft.ProgressRing(),
                    col={"sm": 1, "md": 1, "xl": 1}
                )
            ],
        ),
    )
    page_resize(None)


ft.app(target=main)


# from pytube import YouTube

# # URL del video que deseas descargar
# video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

# # Crear objeto YouTube
# yt = YouTube(video_url)

# # Obtener el stream de video de mayor resolución
# video_stream = yt.streams.get_highest_resolution()

# # Descargar el video en el directorio actual
# video_stream.download()

# print(f"Video '{yt.title}' descargado exitosamente!")
