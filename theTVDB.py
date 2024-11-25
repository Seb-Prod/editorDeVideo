import tvdb_v4_official
import requests
tvdb = tvdb_v4_official.TVDB("bb42c9ed-bfdc-4ba7-8eef-6187a81023bd")
# fetching a series
series = tvdb.get_series(121361)
print(series['id'])
#print(series)


url = "https://api4.thetvdb.com/v4/login"
payload = {
    "apikey": "bb42c9ed-bfdc-4ba7-8eef-6187a81023bd"  # Remplacez par votre clé API
}
response = requests.post(url, json=payload)
#print(f"Statut HTTP : {response.status_code}")  # Log du statut
#print(f"Réponse brute : {response.text}")  # Log de la réponse complète
if response.status_code == 200:
    token = response.json().get("data", {}).get("token")
    #print(f"Token obtenu : {token}")
else:
    print(f"Erreur lors de l'authentification : {response.status_code}, {response.text}")
serie_id = 121361 
headers = {
    "Authorization": f"Bearer {token}",  # Remplacez par le token obtenu
    "Accept-Language": "fr"
}
serie_name = "halo"
url = f"https://api4.thetvdb.com/v4/series/{serie_id}/translations/fra"  # Remplacez 12345 par un ID valide

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    serie = data.get("data", {})
    print("Informations de la série :")
    print(f"Titre : {serie.get('name', 'Inconnu')}")
    print(f"Résumé : {serie.get('overview', 'Non disponible')}")
    print(f"Statut : {serie.get('status', 'Non disponible')}")
    print(f"Première diffusion : {serie.get('firstAired', 'Non disponible')}")
    
else:
    print(f"Erreur : {response.status_code}, {response.text}")
  
    
url = f"https://api4.thetvdb.com/v4/series/{serie_id}/episodes"

# Envoi de la requête
response = requests.get(url, headers=headers)
print(f"URL : {url}")
print(f"En-têtes : {headers}")
print(f"Code de statut : {response.status_code}")
print(f"Réponse brute : {response.text}")
# Vérification de la réponse
if response.status_code == 200:
    data = response.json()
    episodes = data.get('data', [])
    
    if episodes:
        print(f"Liste des épisodes de la série avec ID {serie_id}:")
        for episode in episodes:
            # Afficher l'ID de l'épisode, son titre et sa saison
            print(f"Saison {episode['season']}, Épisode {episode['number']}: {episode['name']}")
    else:
        print("Aucun épisode trouvé.")
else:
    print(f"Erreur : {response.status_code}, {response.text}")