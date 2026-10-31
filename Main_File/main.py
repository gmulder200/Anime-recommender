import json
from Jikan_Scraper_Test import Scraper_Jikan
import SQLite_Db


#connection = sqlite3.connect("anime.db")
#cur = connection.cursor()
#cur.execute("PRAGMA FOREIGN_KEYS = ON")
#connection.commit()
#connection.close()
# MAL_ID : 52991, 



anime = Scraper_Jikan(54492)
SQLite_Db.add_anime(anime)

genres = SQLite_Db.get_anime_genres(54492)


studios = SQLite_Db.get_anime_studio(54492)


themes = SQLite_Db.get_anime_themes(54492)

demographics = SQLite_Db.get_anime_demographics(54492)






info = SQLite_Db.get_anime(52991)
print(info)






