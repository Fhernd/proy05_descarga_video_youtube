import os
import re

from dotenv import load_dotenv
import flet as ft
import requests


def es_url_youtube(url: str) -> bool:
    """
    Verifica si la cadena de texto es una URL válida.
    
    Args:
        url (str): Cadena de texto a verificar.
        
    Returns:
        bool: True si es una URL válida, False en caso contrario.
    """
    regex = r'^(https?://)?(www\.)?(m\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    return re.match(regex, url) is not None


def existe_video(video_id, api_key):
    # Construye la URL de la API
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=id"
    
    # Hace la solicitud a la API
    response = requests.get(url)
    data = response.json()
    
    # Si 'items' en la respuesta es una lista vacía, el video no existe
    if not data.get('items'):
        return False
    return True


def es_url(url: str) -> bool:
    """
    Verifica si la cadena de texto es una URL válida.
    
    Args:
        url (str): Cadena de texto a verificar.
        
    Returns:
        bool: True si es una URL válida, False en caso contrario.
    """
    regex = r'^(https?://)?(www\.)?'
    return re.match(regex, url) is not None


def main(page: ft.Page):
    
    load_dotenv()
    youtube_api_key = os.getenv("API_KEY")
    
    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[
            ft.TextButton("Ok", on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def descargar(event):
        url_id = txt_url_id.current.value
        
        if not es_url_youtube(url_id) and not es_url_youtube(f"https://www.youtube.com/watch?v={url_id}"):
            dlg_modal.title = ft.Text("Advertencia")
            dlg_modal.content = ft.Text('La URL ingresada no es válida. Debe ser una URL de YouTube.')
            
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()
            return
        
        if es_url(url_id):
            url_id = url_id.split("=")[-1]
        
        if not existe_video(url_id, youtube_api_key):
            dlg_modal.title = ft.Text("Advertencia")
            dlg_modal.content = ft.Text('El video no existe.')
            
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()
            return
        
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


if __name__ == "__main__":
    ft.app(target=main)


# from pytube import YouTube

# # URL del video que deseas descargar
# video_url = 'https://www.youtube.com/watch?v=dQw4w9WgXCq'

# # Crear objeto YouTube
# yt = YouTube(video_url)

# # Obtener el stream de video de mayor resolución
# video_stream = yt.streams.get_highest_resolution()

# # Descargar el video en el directorio actual
# video_stream.download()

# print(f"Video '{yt.title}' descargado exitosamente!")
