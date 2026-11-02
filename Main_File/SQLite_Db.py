import sqlite3
from Tenrai_API_Animedata import get_anime_id, Scraper_Tenrai
import time
import requests

def create_database():

    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
    cur.execute("PRAGMA FOREIGN_KEYS = ON")

    ### Creation of Main Table Containing most information which doesnt contain multiple catagories as for example Genres
    cur.execute("""CREATE TABLE IF NOT EXISTS anime (
        mal_id INTEGER PRIMARY KEY,
        main_title TEXT NOT NULL,
        english_title TEXT,
        score REAL,
        episodes INTEGER,
        airing_status TEXT,
        approved INTEGER NOT NULL CHECK (approved IN (0, 1)),
        type TEXT,
        score_votes INTEGER,
        favorites INTEGER,
        duration TEXT,
        year INTEGER,
        synopsis TEXT
    )""")

    ### Creation of the Genre Table 
    cur.execute("""CREATE TABLE IF NOT EXISTS genre(
        genre_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )""")

    ### Creation of the connection table between the Genre Table and the Anime Table
    cur.execute("""CREATE TABLE IF NOT EXISTS AnimeGenre(
        mal_id INTEGER,
        genre_id INTEGER,
        FOREIGN KEY (mal_id)
        REFERENCES anime(mal_id),
        FOREIGN KEY(genre_id)
        REFERENCES genre(genre_id),
        PRIMARY KEY (mal_id,genre_id)
    )""")

    ### Creation of the Studio Table 
    cur.execute("""CREATE TABLE IF NOT EXISTS studio(
        studio_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )""")

    ### Creation of the connection table between the Studio Table and the Anime Table
    cur.execute("""CREATE TABLE IF NOT EXISTS AnimeStudio(
        mal_id INTEGER,
        studio_id INTEGER,
        FOREIGN KEY (mal_id)
        REFERENCES anime(mal_id),
        FOREIGN KEY(studio_id)
        REFERENCES studio(studio_id),
        PRIMARY KEY (mal_id,studio_id)
    )""")

    ### Creation of the Themes Table 
    cur.execute("""CREATE TABLE IF NOT EXISTS themes(
        theme_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )""")

    ### Creation of the connection table between the Themes Table and the Anime Table
    cur.execute("""CREATE TABLE IF NOT EXISTS AnimeThemes(
        mal_id INTEGER,
        theme_id INTEGER,
        FOREIGN KEY (mal_id)
        REFERENCES anime(mal_id),
        FOREIGN KEY(theme_id)
        REFERENCES themes(theme_id),
        PRIMARY KEY (mal_id,theme_id)
    )""")

    ### Creation of the Demographics Table 
    cur.execute("""CREATE TABLE IF NOT EXISTS demographic(
        demographic_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )""")

    ### Creation of the connection table between the Demographics Table and the Anime Table
    cur.execute("""CREATE TABLE IF NOT EXISTS AnimeDemographic(
        mal_id INTEGER,
        demographic_id INTEGER,
        FOREIGN KEY (mal_id)
        REFERENCES anime(mal_id),
        FOREIGN KEY(demographic_id)
        REFERENCES demographic(demographic_id),
        PRIMARY KEY (mal_id,demographic_id)
    )""")

def get_anime_genres(MAL_id):
    #Initiate connection and cursor
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()

    #Create a Selector which gives genres based on mal_id
    cur.execute("""
        SELECT genre.name
        FROM AnimeGenre
        JOIN genre ON genre.genre_id = AnimeGenre.genre_id
        WHERE AnimeGenre.mal_id = ?
        """, (MAL_id,))

    #Fetch the genres and return them
    genres = cur.fetchall()
    connection.close()
    return [row[0] for row in genres]

def get_anime_studio(MAL_id):
    #Initiate connection and cursor
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
    
    #Create a Selector which gives studio based on mal_id
    cur.execute("""
        SELECT studio.name
        FROM AnimeStudio
        JOIN studio ON studio.studio_id = AnimeStudio.studio_id
        WHERE AnimeStudio.mal_id = ?
        """, (MAL_id,))
    #Fetch the studios and return them
    studios = cur.fetchall()
    connection.close()
    return [row[0] for row in studios]

def get_anime_themes(MAL_id):
    #Initiate connection and cursor
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
        
    #Create a Selector which gives theme based on mal_id
    cur.execute("""
        SELECT themes.name
        FROM AnimeThemes
        JOIN themes ON themes.theme_id = AnimeThemes.theme_id
        WHERE AnimeThemes.mal_id = ?
        """, (MAL_id,))
    #Fetch the theme and return them
    themes = cur.fetchall()
    connection.close()
    return [row[0] for row in themes]

def get_anime_demographics(MAL_id):
    #Initiate connection and cursor
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
        
    #Create a Selector which gives demographic based on mal_id
    cur.execute("""
        SELECT demographic.name
        FROM AnimeDemographic
        JOIN demographic ON demographic.demographic_id = AnimeDemographic.demographic_id
        WHERE AnimeDemographic.mal_id = ?
        """, (MAL_id,))
    #Fetch the demographic and return them
    demographic = cur.fetchall()
    connection.close()
    return [row[0] for row in demographic]
    
def add_anime(anime):
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("""INSERT INTO anime(mal_id,main_title,english_title,score,episodes,airing_status,approved,type,score_votes,favorites,duration,year,synopsis)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT(mal_id) DO UPDATE SET
        main_title=excluded.main_title,
        english_title=excluded.english_title,
        score=excluded.score,
        episodes=excluded.episodes,
        airing_status=excluded.airing_status,
        approved=excluded.approved,
        type=excluded.type,
        score_votes=excluded.score_votes,
        favorites=excluded.favorites,
        duration=excluded.duration,
        year=excluded.year,
        synopsis=excluded.synopsis
    """,(anime["mal_id"],anime["main_title"],anime["english_title"],anime["score"],anime["episodes"],anime["airing_status"],anime["approved"],anime["type"],anime["score_votes"],anime["favorites"],anime["duration"],anime["year"],anime["synopsis"]) )

    cur.execute("DELETE FROM AnimeGenre WHERE mal_id = ?", (anime["mal_id"],))
    cur.execute("DELETE FROM AnimeStudio WHERE mal_id = ?", (anime["mal_id"],))
    cur.execute("DELETE FROM AnimeThemes WHERE mal_id = ?", (anime["mal_id"],))
    cur.execute("DELETE FROM AnimeDemographic WHERE mal_id = ?", (anime["mal_id"],))



    #For Loop to add genre to its own table(creating Genre_id in the process) and then also fetching that Genre_ID and then adding that and MAL_ID to the connection TABLE
    for genre in anime["genres"]:
        cur.execute("""INSERT OR IGNORE INTO genre(name)
        VALUES(?)""",(genre,))
        res = cur.execute("""SELECT genre_id
        FROM genre
        WHERE name = ?
        """,(genre,))

        genre_id = res.fetchone()[0]

        cur.execute("""INSERT OR IGNORE INTO AnimeGenre(mal_id,genre_id)
        VALUES(?,?)
          """,(anime["mal_id"],genre_id))


    #For Loop to add studio to its own table(creating studio_id in the process) and then also fetching that studio_id and then adding that and MAL_ID to the connection TABLE
    for studio in anime["studio_name"]:
        cur.execute("""INSERT OR IGNORE INTO studio(name)
        VALUES(?)""",(studio,))
        res = cur.execute("""SELECT studio_id
        FROM studio
        WHERE name = ?
        """,(studio,))

        studio_id = res.fetchone()[0]

        cur.execute("""INSERT OR IGNORE INTO AnimeStudio(mal_id,studio_id)
        VALUES(?,?)
          """,(anime["mal_id"],studio_id))
    
    #For Loop to add themes to its own table(creating theme_id in the process) and then also fetching that theme_id and then adding that and MAL_ID to the connection TABLE
    for theme in anime["themes"]:
        cur.execute("""INSERT OR IGNORE INTO themes(name)
        VALUES(?)""",(theme,))
        res = cur.execute("""SELECT theme_id
        FROM themes
        WHERE name = ?
        """,(theme,))

        theme_id = res.fetchone()[0]

        cur.execute("""INSERT OR IGNORE INTO AnimeThemes(mal_id,theme_id)
        VALUES(?,?)
          """,(anime["mal_id"],theme_id))    

    #For Loop to add themes to its own table(creating theme_id in the process) and then also fetching that theme_id and then adding that and MAL_ID to the connection TABLE
    for demographic in anime["demographics"]:
        cur.execute("""INSERT OR IGNORE INTO demographic(name)
        VALUES(?)""",(demographic,))
        res = cur.execute("""SELECT demographic_id
        FROM demographic
        WHERE name = ?
        """,(demographic,))

        demographic_id = res.fetchone()[0]

        cur.execute("""INSERT OR IGNORE INTO AnimeDemographic(mal_id,demographic_id)
        VALUES(?,?)
          """,(anime["mal_id"],demographic_id))        
    connection.commit()
    connection.close()

def get_anime(mal_id):
    connection = sqlite3.connect("anime.db")
    connection.row_factory = sqlite3.Row
    cur = connection.cursor()

    cur.execute("""
        SELECT *
        FROM anime
        WHERE anime.mal_id = ?
        """, (mal_id,))

    anime_info = cur.fetchone()
    if anime_info is not None:
        anime_info = dict(anime_info)

        genres = get_anime_genres(mal_id)
        studio = get_anime_studio(mal_id)
        themes = get_anime_themes(mal_id)
        demographics = get_anime_demographics(mal_id)
    
        anime_info["genres"]= genres
        anime_info["studio_name"]= studio
        anime_info["themes"]= themes
        anime_info["demographics"]= demographics

    
    connection.close()
    return(anime_info)

def anime_count():

    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()

    cur.execute("SELECT COUNT(*) FROM anime")
    count = cur.fetchone()[0]

    connection.close()
    return count

def genre_count():
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
    
    cur.execute("SELECT COUNT(*) FROM genre")
    count = cur.fetchone()[0]
    
    connection.close()
    return count
    
def studio_count():
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
    
    cur.execute("SELECT COUNT(*) FROM studio")
    count = cur.fetchone()[0]
    
    connection.close()
    return count
    
def theme_count():
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
    
    cur.execute("SELECT COUNT(*) FROM themes")
    count = cur.fetchone()[0]
    
    connection.close()
    return count

def demographic_count():
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()
    
    cur.execute("SELECT COUNT(*) FROM demographic")
    count = cur.fetchone()[0]
    
    connection.close()
    return count

def get_anime_name(mal_id):
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()

    cur.execute("""
                SELECT anime.main_title
                FROM anime
                WHERE anime.mal_id = ?
                """, (mal_id,))
    anime_title = cur.fetchone()
    connection.close()
    return anime_title[0] if anime_title is not None else None

def get_all_mal_ID():
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()

    cur.execute("SELECT mal_id FROM anime")
    mal_ids = [row[0] for row in cur.fetchall()]

    return mal_ids
    


def ImportUpdate_database():
    connection = sqlite3.connect("anime.db")
    cur = connection.cursor()

    print("= Anime Database Importer =")
    print("1. Add New Anime")
    print("2. Update Anime")
    print("3. Update and Add Anime")

    choice = input("Choose an option (1-3): ")
    mal_data = get_anime_id()
    counter= 0
    match choice:
        case "1":
            for mal_id in mal_data["data"]:
                cur.execute("""SELECT anime.mal_id 
                                        FROM anime
                                        WHERE anime.mal_id = ? 
                                        """,(mal_id,))
                mal_check = cur.fetchone()
                counter +=1
                
                if mal_check is None:
                    try:
                        anime_info = Scraper_Tenrai(mal_id)
                        if anime_info is not None: 
                            add_anime(anime_info)
                            time.sleep(0.25)
                            print(f"[{counter}/{mal_data['total']}] Added: {anime_info['main_title']}")
                        else: 
                            print(f"[{counter}/{mal_data['total']}] Skipped Due to repearted 429 Response, MAL ID {mal_id}")
                    except requests.exceptions.Timeout:
                        print(f"[{counter}/{mal_data['total']}] Timeout: {mal_id}")
                    except requests.exceptions.HTTPError as e:
                        print(f"[{counter}/{mal_data['total']}] HTTP error: {e}")
                    except requests.exceptions.RequestException as e:
                        print(f"[{counter}/{mal_data['total']}] Request failed: {e}") 
                else:
                    anime_name =  get_anime_name(mal_id)
                    print(f"[{counter}/{mal_data['total']}] Skipped: {anime_name}")

        case "2":
            mal_id_dblist = get_all_mal_ID()

            for mal_id in mal_id_dblist:
                counter +=1
                try:
                    anime_info = Scraper_Tenrai(mal_id)
                    if anime_info is not None:
                        add_anime(anime_info)
                        time.sleep(0.25)
                        print(f"[{counter}/{len(mal_id_dblist)}] Updated: {anime_info['main_title']}")
                    else: 
                        print(f"[{counter}/{len(mal_id_dblist)}] Skipped Due to repearted 429 Response, MAL ID {mal_id}")
                except requests.exceptions.Timeout:
                    print(f"[{counter}/{len(mal_id_dblist)}] Timeout: {mal_id}")
                except requests.exceptions.HTTPError as e:
                    print(f"[{counter}/{len(mal_id_dblist)}] HTTP error: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"[{counter}/{len(mal_id_dblist)}] Request failed: {e}") 

        case "3":
            for mal_id in mal_data["data"]:
                counter +=1
                try:
                    anime_info = Scraper_Tenrai(mal_id)
                    if anime_info is not None: 
                        add_anime(anime_info)
                        time.sleep(0.25)
                        print(f"[{counter}/{mal_data['total']}] Added: {anime_info['main_title']}")
                    else: 
                        print(f"[{counter}/{mal_data['total']}] Skipped Due to repearted 429 Response, MAL ID {mal_id}")
                except requests.exceptions.Timeout:
                    print(f"[{counter}/{mal_data['total']}] Timeout: {mal_id}")
                except requests.exceptions.HTTPError as e:
                    print(f"[{counter}/{mal_data['total']}] HTTP error: {e}")
                except requests.exceptions.RequestException as e:
                    print(f"[{counter}/{mal_data['total']}] Request failed: {e}") 

        case _:
            print("Invalid selection")
    connection.close()




