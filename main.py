import flet as ft
import edit_video as app

def main(page: ft.Page):
    page.title = "Image Manipulator LITE"

    # Fonction de callback lorsqu'un fichier est sélectionné
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
           for file in e.files:
                app.get_video_name(file.path)
                #print(file.path)
                #print(file.name)

    # Initialisation du FilePicker avec filtre pour fichier video
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    
    
    page.add(
        ft.ElevatedButton("Sélectionner des fichiers", on_click=lambda _: file_picker.pick_files(
            allow_multiple=True,  # Autorise plusieurs fichiers
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["mp4", "mkv", "avi"] 
        ))
    )
#app.get_video_name("/Volumes/Macintosh HD/Users/seb/Downloads/01 Tamara.mp4")
app.get_video_name("/Volumes/Macintosh HD/Users/seb/Downloads/06 Prudence.mp4")

#ft.app(target=main)