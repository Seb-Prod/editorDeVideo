import base64
from dataclasses import dataclass
import re
import requests
from tvdb_v4_official import TVDB

api_key = "bb42c9ed-bfdc-4ba7-8eef-6187a81023bd"  # Obtenue sur TheTVDB
tvdb = TVDB(api_key)


@dataclass
class TvData:
    series: tuple
    saison: int
    episode:int


@dataclass
class serie_info:
    id: str
    nom: str
    resume: str
    image:str
    
@dataclass
class info_episode:
    id: int
    saison: int
    num:int


def find_serie_name(file_name)->TvData:

    info = extract_info(file_name)
    if info:
        name = remove_point(info['series'])
        series = tvdb.search(name)

        # boucle qui récupère le noms des séries trouvé et les ID
        tableau_liste_series = []
        for serie in series:
            serie_id = serie['tvdb_id']
            try:
                serie_resume = serie['overviews']['fra']
            except:
                serie_resume = serie['overviews']['eng']
            try:
                serie_nom = serie['translations']['fra']
            except:
                serie_nom = serie['translations']['eng']
                
            serie_img = url_to_base64(serie['thumbnail'])
                
            tableau_liste_series.append(serie_info(id=serie_id, nom=serie_nom, resume=serie_resume, image=serie_img))
            
        return TvData(series=tableau_liste_series, saison=info['season'], episode=info['episode'])
    else:
        return []

def find_episodes(serie_id:int):
    info = tvdb.get_series_episodes(serie_id, page=0)
    tableau_episode =[]
    for ep in info["episodes"]:
        tableau_episode.append(info_episode(id=ep['id'], saison=ep['seasonNumber'],num=ep['number']))
    
    return tableau_episode

def fetch_episode(id) -> str:
    episode = tvdb.get_episode_translation(id=id, lang="fra")
    return episode['overview']

def remove_point(name):
    return name.replace(".", " ")


def extract_info(filename):
    pattern = r"^(?P<series>.+?)\.S(?P<season>\d{2})E(?P<episode>\d{2})\.(?P<language>[A-Z]+)\.(?P<qualite>\w+)\.(?P<codec>\w+)-(?P<source>\w+)\.\w+\.(?P<extension>\w+)$"

    match = re.match(pattern, filename)
    if match:
        return match.groupdict()
    else:
        return None

def url_to_base64(url):
  # Realiza una solicitud HTTP para obtener la imagen
  response = requests.get(url)
  response.raise_for_status()  # Levanta una excepción si la solicitud falla

  # Codifica la imagen en base64
  img_base64 = base64.b64encode(response.content).decode('utf-8')
  return img_base64