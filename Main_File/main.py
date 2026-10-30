import json
from Jikan_Scraper_Test import Scraper_Jikan
from SQLite_Db import add_anime, get_anime_genres


#connection = sqlite3.connect("anime.db")
#cur = connection.cursor()
#cur.execute("PRAGMA FOREIGN_KEYS = ON")
#connection.commit()
#connection.close()
# MAL_ID : 52991, 



anime = Scraper_Jikan(61967)
add_anime(anime)

genres = get_anime_genres(52991)
print(genres)





