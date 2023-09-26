import os
import re

from dotenv import load_dotenv
import flet as ft
from pytube import YouTube
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
    """
    Verifica si el vídeo existe.
    
    Args:
        video_id (str): ID del vídeo.
        api_key (str): API Key de YouTube.
    
    Returns:
        bool: True si el vídeo existe, False en caso contrario.
    """
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=id"
    
    response = requests.get(url)
    data = response.json()
    
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


def extraer_id_video(url):
    """
    Extrae el ID del vídeo de YouTube a partir de la URL proporcionada.
    
    :param url: URL del vídeo de YouTube.
    :return: ID del vídeo o None si la URL no es válida.
    """
    # Esta expresión regular cubre varios formatos de URL de YouTube.
    pattern = (
        r"(?:https?://)?(?:www\.)?"
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|www\.youtube\.com/v/)"
        r"([^&\n?]+)"
    )
    match = re.match(pattern, url)
    return match.group(1) if match else None


def descargar_video(video_id):
    """
    Descarga el vídeo de YouTube.
    
    :param video_id: ID del vídeo de YouTube.
    """

    # URL del video que deseas descargar
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    # Crear objeto YouTube
    yt = YouTube(video_url)

    # Obtener el stream de video de mayor resolución
    video_stream = yt.streams.get_highest_resolution()

    # Descargar el video en el directorio actual
    video_stream.download()

    print(f"Video '{yt.title}' descargado exitosamente!")


def main(page: ft.Page):
    """
    Función principal de la aplicación.
    
    Args:
        page (ft.Page): Página de la aplicación.
    """
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
    
    def save_file_result(e: ft.FilePickerResultEvent):
        ruta = e.path if e.path else "Cancelled!"
        print(ruta)
    
    dlg_guardar_archivo = ft.FilePicker(on_result=save_file_result)
    
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
            video_id = extraer_id_video(url_id)
        else:
            video_id = url_id
        
        if not existe_video(video_id, youtube_api_key):
            dlg_modal.title = ft.Text("Advertencia")
            dlg_modal.content = ft.Text('El video no existe.')
            
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()
            return
        
        dlg_guardar_archivo.save_file()
        # descargar_video(video_id)
        
        
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
    
    page.overlay.extend([dlg_guardar_archivo])


if __name__ == "__main__":
    ft.app(target=main)
