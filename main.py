import flet as ft
import edit_video as app


#metaData = app.get_metadata("/Volumes/Macintosh HD/Users/seb/Downloads/06 Prudence.mp4")
metaData = app.get_metadata("/Volumes/Macintosh HD/Users/seb/Downloads/Interior.Chinatown.S01E02.FRENCH.WEBRip.x264-Wawacity.run.mp4")

def main(page: ft.Page):
    page.title = "MyTV"
    
    # Fonction de callback lorsqu'un fichier est sélectionné
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
           for file in e.files:
                app.get_video_name(file.path)

    # Fonction de callback lorsque la date est changé
    def handle_change(e):
        input_date.text=f"{e.control.value.strftime('%d-%m-%Y')}"
        page.add()

    # Initialisation du FilePicker avec filtre pour fichier video
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)
    
    # Initialisation des Input de saisie
    input_episode_name = ft.TextField(label="Titre", value=metaData.name, height=30, text_vertical_align=ft.VerticalAlignment.START, text_size=12)
    input_show_name = ft.TextField(label="Série", value=metaData.artist, height=30, text_vertical_align=ft.VerticalAlignment.START, text_size=12)
    input_season = ft.TextField(label="Saison", value=metaData.tv_season, width=80,height=30, text_vertical_align=ft.VerticalAlignment.START, text_size=12)
    input_episode= ft.TextField(label="Episode", value=metaData.tv_episode, width=80, height=30, text_vertical_align=ft.VerticalAlignment.START, text_size=12)
    input_genre = ft.TextField(label="Genre", value=metaData.genre, height=30, text_vertical_align=ft.VerticalAlignment.START, text_size=12)
    input_episode_description = ft.TextField(label="Description courte", value=metaData.description, multiline=True, min_lines=3, max_lines=3, height=90, text_vertical_align=ft.VerticalAlignment.START, text_size=12)
    input_episode_long_description = ft.TextField(label="Description longue", value=metaData.long_description, multiline=True, min_lines=3, max_lines=3, height=90, text_vertical_align=ft.VerticalAlignment.START, text_size=12)
    input_show_description = ft.TextField(label="Description série", value=metaData.tv_description, multiline=True, min_lines=3, max_lines=3, height=90, text_vertical_align=ft.VerticalAlignment.START, text_size=12)
    
    input_date =ft.ElevatedButton(
            metaData.year,
            icon=ft.icons.CALENDAR_MONTH,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            height=30,
            width=160,
            on_click=lambda e: page.open(
                ft.DatePicker(
                    on_change=handle_change,
                )
            ),
        )
    
    imgage = ft.Image(
        src_base64=metaData.image,
        width=500,
        height=500,
        fit=ft.ImageFit.CONTAIN,
    )
    
    # Affichage
    page.add(
        ft.Row([
            ft.Column(
                [input_episode_name, input_show_name, ft.Row([input_season, input_episode, input_date]), input_genre, input_episode_description, input_episode_long_description, input_show_description], width=340),
            ft.Column([imgage])
            ])
    )
   


ft.app(target=main)
