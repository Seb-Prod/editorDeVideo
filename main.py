import plistlib
import flet as ft
import custun_control as custum
import edit_video as app
import theTVDB as tv

video_name = ""
nom_serie = ""
new_index = 0
metaData:app.dataclass = ""
metaDataTVDB:tv.TvData = ""
metaDataEpisode:tv.info_episode = ""


def main(page: ft.Page):
    page.title = "MyTV"
    page.window.width = 1080
    page.window.height = 650
    page.window.center()
    
    # Fonction de callback lorsque la date est changé
    def dropdown_changed(e):
        global new_index
        for i in range(0, len(metaDataTVDB.series)):
            datas: tv.serie_info = metaDataTVDB.series[i]
            if e.data == datas.nom:
                new_index = i
        recuperation_liste_des_episode(new_index)
            
        

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

    # Fonction de callback lorsque que l'on charge les donées depuis l'api
    def button_tvDB_clicked():
        get_meta_tv_db()
        set_option_of_serie_list()
        recuperation_liste_des_episode(0)
        print(f"{list_season.value} x {list_episode.value}")
        for episode in metaDataEpisode:
            my_episode:tv.info_episode = episode
            if int(my_episode.saison) == int(list_season.value) and int(my_episode.num) == int(list_episode.value):
                
                input_episode_description.value = tv.fetch_episode(int(my_episode.id))
        page.update()

    # Fonction qui met à jour les inputs
    def set_input_value():
        list_serie_name.options.clear()
        list_serie_name.options.append(
            ft.dropdown.Option(metaData.album_artist))
        list_serie_name.value = metaData.album_artist
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

    # Extration des donnes suplémentaire du xml
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

    # Récupération des données depuis theTvDB
    def get_meta_tv_db():
        global metaDataTVDB
        metaDataTVDB = tv.find_serie_name(video_name)
    
    # initialisation des listes saison et épisode
    def recuperation_liste_des_episode(index:int):
        global nom_serie, metaDataEpisode
        datas:tv.serie_info = metaDataTVDB.series[index]
        nom_serie = datas.nom
        list_serie_name.value = datas.nom
        input_show_description.value = datas.resume
        image.src_base64 = datas.image
        
        metaDataEpisode = tv.find_episodes(int(datas.id))
        
        initialisation_liste_saison()
        initialisation_liste_episode()
       
        list_season.value = int(metaDataTVDB.saison)
        list_episode.value = int(metaDataTVDB.episode)
        page.update()
    
    # Remplie la liste des saisons
    def initialisation_liste_saison():
        tableau_season = []
        for episode in metaDataEpisode:
            my_episode:tv.info_episode = episode
            tableau_season.append(my_episode.saison)
        tableau_season = list(set(tableau_season))
        set_option_of_episode(list_season, tableau_season)

    # Renplie la liste des épisode
    def initialisation_liste_episode():
        tableau_episode = []
        for episode in metaDataEpisode:
            my_episode:tv.info_episode = episode
            if(my_episode.saison == int(metaDataTVDB.saison)):
                tableau_episode.append(my_episode.num)
        tableau_episode = list(set(tableau_episode))
        set_option_of_episode(list_episode, tableau_episode)

    def set_option_of_serie_list():
        list_serie_name.options.clear()
        for item in metaDataTVDB.series:
            datas: tv.serie_info = item
            list_serie_name.options.append(ft.dropdown.Option(datas.nom))

    def set_option_of_episode(list:ft.dropdown, values: tuple):
        list.options.clear()
        for value in values:
            list.options.append(ft.dropdown.Option(value))

    # Le popup du choix du fichier à ajouter
    file_picker_video = ft.FilePicker(on_result=open_video)
    page.overlay.append(file_picker_video)

    # Ouverture automatique pour test
    def testAuto():
        global metaData, video_name
        #video_name = "Cats.Eyes.2024.S01E06.FRENCH.WEBRip.x264-Wawacity.run.mp4"
        #video_name = "Interior.Chinatown.S01E02.FRENCH.WEBRip.x264-Wawacity.run.mp4"
        #video_name = "The.Helicopter.Heist.S01E01.FRENCH.WEBRip.x264-Wawacity.run.mp4"
        video_name = "Special.Ops.Lioness.S02E06.FRENCH.WEBRip.x264-Wawacity.run.mp4"
        label_nom_fichier.value = video_name
        metaData = app.get_metadata(
            f"/Volumes/Macintosh HD/Users/seb/Downloads/{video_name}")
        set_input_value()

    # Initialisation du bouton d'ouverture d'un fichier vidéo
    button_open_video_picker = custum.Button(
        "Ouvrir video", icon=ft.icons.LOCAL_MOVIES)
    button_open_video_picker.on_click = lambda e: testAuto()
    # button_open_video_picker.on_click=lambda e: file_picker_video.pick_files(
    #         allow_multiple=False, allowed_extensions=["avi", "mp4", "mkv"], dialog_title="Sélectionnez une video")

    # Initialisation du bouton d'ouverture du résultat de la requettre TheTvDB
    button_TheTvDB = custum.Button("Metadonées")
    button_TheTvDB.on_click = lambda e: button_tvDB_clicked()

    # Initialisation des Input de saisie
    list_serie_name = custum.ListDropDown()
    list_serie_name.width = 340
    list_season = custum.ListDropDown()
    list_episode = custum.ListDropDown()
    
    list_serie_name.on_change = dropdown_changed
    input_episode_name = custum.TextField(label="Titre")
    input_season = custum.TextField(label="Saison")
    input_season.width = 80
    input_episode = custum.TextField(label="Episode")
    input_episode.width = 80
    input_genre = custum.TextField(label="Genre")
    input_episode_description = custum.TextFieldMultiLine(
        label="Description courte")
    input_episode_long_description = custum.TextFieldMultiLine(
        label="Description longue")
    input_show_description = custum.TextFieldMultiLine(
        label="Description série")
    button_open_date_picker = custum.Button(
        '24-11-2024', ft.icons.CALENDAR_MONTH)
    button_open_date_picker.on_click = lambda e: page.open(
        ft.DatePicker(
            on_change=handle_change,
        )
    )

    # Initialisation de la listView pour les informations complémantaires
    listView_more_info = ft.ListView(
        expand=1, spacing=10, padding=0, height=100)

    # Initialisation de l'image d'aperçus
    image = ft.Image(width=340, height=340)

    # Initialisation du label avec le nom du fichier en cours de consultation
    label_nom_fichier = ft.Text("Aucun fichier video d'ouvert")

    
                                        

    # Affichage
    page.add(
        ft.Column([
            ft.Row([button_open_video_picker, button_TheTvDB, label_nom_fichier]),
            ft.Row([
                ft.Column(
                    [list_serie_name, input_episode_name, ft.Row([list_season, list_episode, button_open_date_picker]), input_genre, input_episode_description, input_episode_long_description, input_show_description, listView_more_info], width=340),
                ft.Column([image], expand=1)
            ])
        ])

    )


ft.app(target=main)
