import plistlib
import flet as ft
import custun_control as custum
import edit_video as app
import theTVDB as tv

video_name = "Halo.S01E01.FRENCH.WEBRip.x264-Wawacity.run.mp4"
# metaData = app.get_metadata(
#    "/Volumes/Macintosh HD/Users/seb/Downloads/06 Prudence.mp4")
metaData = app.get_metadata(
    "/Volumes/Macintosh HD/Users/seb/Downloads/Interior.Chinatown.S01E01.FRENCH.WEBRip.x264-Wawacity.run.mp4")


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
        global metaData, video_name
        if not e.files == None:
            for file in e.files:
                video_name = file.name
                label_nom_fichier.value = file.name
                metaData = app.get_metadata(file.path)
                set_input_value()

    # Fonction qui met à jour les inputs
    def set_input_value():
        list_serie_name.options.clear()
        list_serie_name.options.append(ft.dropdown.Option(metaData.album_artist))
        list_serie_name.value=metaData.album_artist
        input_episode_name.value = metaData.name
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

    # Exxtration des donnes suplémentaire du xml
    def extraire_donnees_xml(xml_data: str):
        if (xml_data):
            data = plistlib.loads(xml_data)
            keys = data.keys()
            for key in keys:
                temporary = ""
                for cast in data[key]:
                    temporary = temporary + cast['name'] + ", "

                new_string = temporary[:-2]
                listView_more_info.controls.append(custum.TextFieldMultiLine(
                    label=key, value=new_string))

    # Le popup du choix du fichier à ajouter
    file_picker_video = ft.FilePicker(on_result=open_video)
    page.overlay.append(file_picker_video)

    # Initialisation du bouton d'ouverture d'un fichier vidéo
    button_open_video_picker = custum.Button("Ouvrir video",icon=ft.icons.LOCAL_MOVIES)
    button_open_video_picker.on_click=lambda e: file_picker_video.pick_files(
            allow_multiple=False, allowed_extensions=["avi", "mp4", "mkv"], dialog_title="Sélectionnez une video")

    # Initialisation du bouton d'ouverture du résultat de la requettre TheTvDB
    button_TheTvDB = custum.Button("Metadonées")
    button_TheTvDB.on_click = lambda e: set_option_of_serie_list()

    # Initialisation des Input de saisie
    list_serie_name = custum.ListDropDown()
    input_episode_name = custum.TextField(label="Titre")
    input_season = custum.TextField(label="Saison")
    input_season.width = 80
    input_episode = custum.TextField(label="Episode")
    input_episode.width = 80
    input_genre = custum.TextField(label="Genre")
    input_episode_description = custum.TextFieldMultiLine(label="Description courte")
    input_episode_long_description = custum.TextFieldMultiLine(label="Description longue")
    input_show_description = custum.TextFieldMultiLine(label="Description série")
    button_open_date_picker = custum.Button('24-11-2024', ft.icons.CALENDAR_MONTH)
    button_open_date_picker.on_click=lambda e: page.open(
            ft.DatePicker(
                on_change=handle_change,
            )
        )
   
    # Initialisation de la listView pour les informations complémantaires
    listView_more_info = ft.ListView(expand=1, spacing=10, padding=0, height=100)

    # Initialisation de l'image d'aperçus
    image = ft.Image(width=340,height=340)

    # Initialisation du label avec le nom du fichier en cours de consultation
    label_nom_fichier = ft.Text("Aucun fichier video d'ouvert")

    def set_option_of_serie_list():
        tv.find_serie_name("d")
        # list_serie_name.options.clear()
        # list_tv_show = tv.find_serie_name(video_name)
        # for item in list_tv_show:
        #      list_serie_name.options.append(ft.dropdown.Option(item['name']))
            
        # list_serie_name.value = list_tv_show[0]['name']
        # tv.find_episode(int(list_tv_show[0]['tvdb_id']))
        # print(list_tv_show[0]['tvdb_id'])
        # list_serie_name.update()
        

    # Affichage
    page.add(
        ft.Column([
            ft.Row([button_open_video_picker, button_TheTvDB, label_nom_fichier]),
            ft.Row([
                ft.Column(
                    [list_serie_name,input_episode_name, ft.Row([input_season, input_episode, button_open_date_picker]), input_genre, input_episode_description, input_episode_long_description, input_show_description, listView_more_info], width=340),
                ft.Column([image], expand=1)
            ])
        ])

    )

ft.app(target=main)
