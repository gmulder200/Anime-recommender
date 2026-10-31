import json
from Tenrai_API_Animedata import Scraper_Tenrai
import SQLite_Db


#connection = sqlite3.connect("anime.db")
#cur = connection.cursor()
#cur.execute("PRAGMA FOREIGN_KEYS = ON")
#connection.commit()
#connection.close()
# MAL_ID : 52991, 




anime = Scraper_Tenrai(918)
SQLite_Db.add_anime(anime)

genres = SQLite_Db.get_anime_genres(1)


studios = SQLite_Db.get_anime_studio(1)


themes = SQLite_Db.get_anime_themes(1)

demographics = SQLite_Db.get_anime_demographics(1)

print(SQLite_Db.anime_count())
print(SQLite_Db.genre_count())
print(SQLite_Db.studio_count())
print(SQLite_Db.theme_count())
print(SQLite_Db.demographic_count())



info = SQLite_Db.get_anime(918)
#print(info)






