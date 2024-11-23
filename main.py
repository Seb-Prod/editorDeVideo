import plistlib
import flet as ft
import custun_control as custum
import edit_video as app


metaData = app.get_metadata(
    "/Volumes/Macintosh HD/Users/seb/Downloads/06 Prudence.mp4")
# metaData = app.get_metadata( "/Volumes/Macintosh HD/Users/seb/Downloads/Interior.Chinatown.S01E01.FRENCH.WEBRip.x264-Wawacity.run.mp4")


def main(page: ft.Page):
    page.title = "MyTV"
    page.window.width = 1080
    page.window.height = 650
    page.window.center()
    # Fonction de callback lorsque la date est changé

    def handle_change(e):
        button_open_date_picker.text = f"{
            e.control.value.strftime('%d-%m-%Y')}"
        page.add()

    # Fonction de callback lorsque une video est chargé
    def open_video(e: ft.FilePickerResultEvent):
        global metaData
        if not e.files == None:
            for file in e.files:
                label_nom_fichier.value = file.name
                metaData = app.get_metadata(file.path)
                set_input_value()

    # Fonction qui met à jour les inputs
    def set_input_value():
        input_episode_name.value = metaData.name
        input_show_name.value = metaData.artist
        input_season.value = metaData.tv_season
        input_episode.value = metaData.tv_episode
        input_genre.value = metaData.genre
        input_episode_description.value = metaData.description
        input_episode_long_description.value = metaData.long_description
        input_show_description.value = metaData.tv_description
        button_open_date_picker.text = metaData.year
        image.src_base64 = metaData.image
        listView_more_info.controls.clear()
        extraire_donnees_xml(metaData.apple_itunes)
        page.update()

    def extraire_donnees_xml(xml_data: str):
        if(xml_data):
            data = plistlib.loads(xml_data)
            keys = data.keys()
            for key in keys:
                temporary = ""
                for cast in data[key]:
                    temporary = temporary + cast['name'] + ", "
                    
                new_string = temporary[:-2]
                listView_more_info.controls.append(custum.TextField(
                    label=key, value=new_string, multiline=True, min_lines=1, max_lines=1, height=45))


    # Le popup du choix du fichier à ajouter
    file_picker_video = ft.FilePicker(on_result=open_video)
    page.overlay.append(file_picker_video)

    # Initialisation du bouton d'ouverture d'un fichier vidéo
    button_open_video_picker = ft.ElevatedButton(
        "Ouvrir video",
        icon=ft.icons.LOCAL_MOVIES,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=30,
        width=160,
        on_click=lambda e: file_picker_video.pick_files(
            allow_multiple=False, allowed_extensions=["avi", "mp4", "mkv"], dialog_title="Sélectionnez une video")
    )

    # Initialisation des Input de saisie
    input_episode_name = custum.TextField(label="Titre", value=metaData.name)
    input_show_name = custum.TextField(label="Série", value=metaData.artist)
    input_season = custum.TextField(label="Saison", value=metaData.tv_season)
    input_season.width = 80
    input_episode = custum.TextField(
        label="Episode", value=metaData.tv_episode)
    input_episode.width = 80
    input_genre = custum.TextField(label="Genre", value=metaData.genre)
    input_episode_description = custum.TextField(
        label="Description courte", value=metaData.description, multiline=True, min_lines=3, max_lines=3)
    input_episode_description.height = 90
    input_episode_long_description = custum.TextField(
        label="Description longue", value=metaData.long_description, multiline=True, min_lines=3, max_lines=3)
    input_episode_long_description.height = 90
    input_show_description = custum.TextField(
        label="Description série", value=metaData.tv_description, multiline=True, min_lines=3, max_lines=3)
    input_show_description.height = 90
    button_open_date_picker = ft.ElevatedButton(
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

    # Initialisation de la listView pour les informations complémantaires
    listView_more_info = ft.ListView(
        expand=1, spacing=10, padding=0, height=100)

    # Initialisation de l'image d'aperçus
    image = ft.Image(
        src_base64=metaData.image,
        width=340,
        height=100,
        # fit=ft.ImageFit.CONTAIN,
    )

    # Initialisation du label avec le nom du fichier en cours de consultation
    label_nom_fichier = ft.Text("Aucun fichier video d'ouvert")

    # Affichage
    page.add(
        ft.Column([
            ft.Row([button_open_video_picker, label_nom_fichier]),
            ft.Row([
                ft.Column(
                    [input_episode_name, input_show_name, ft.Row([input_season, input_episode, button_open_date_picker]), input_genre, input_episode_description, input_episode_long_description, input_show_description, listView_more_info], width=340),
                ft.Column([image], expand=1)
            ])
        ])

    )


ft.app(target=main)
