import re

import flet as ft


def es_url(url: str) -> bool:
    """
    Verifica si la cadena de texto es una URL válida.
    
    Args:
        url (str): Cadena de texto a verificar.
        
    Returns:
        bool: True si es una URL válida, False en caso contrario.
    """
    regex = r'^(https?://)?(www\.)?(m\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    return re.match(regex, url) is not None


def main(page: ft.Page):
    def descargar(event):
        url_id = txt_url_id.current.value
        
        
        
    txt_url_id = ft.Ref[ft.TextField]()
    
    page.add(
        ft.ResponsiveRow(
            [
                ft.Container(
                    ft.TextField(label="YouTube URL/ID", ref=txt_url_id),
                    padding=5,
                    col={"sm": 9, "md": 9, "xl": 9},
                ),
                ft.Container(
                    ft.FilledButton("Descargar...", icon="add", on_click=descargar),
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
