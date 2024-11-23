from tvdb_v4_official import TVDB

# Initialisation
api_key = "bb42c9ed-bfdc-4ba7-8eef-6187a81023bd"  # Obtenue sur TheTVDB
tvdb = TVDB(api_key)

# Recherche d'une série
search = tvdb.search('Interior Chinatown')
series = search[0]  # On prend le premier résultat

# Récupération d'informations sur la série
series_id = series['id']
print(series_id)
series = tvdb.get_series(425999)
#series_data = tvdb.series_data(series_id, 'en')
print(series)  # Affiche le synopsis