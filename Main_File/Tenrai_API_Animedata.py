import requests
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()
API_KEY = os.getenv("TENRAI_API_KEY")

def Scraper_Tenrai(Mal_ID):

    url = f'https://api.tenrai.org/v1/anime/{Mal_ID}/full'
    headers = {'X-Server-Key': API_KEY}

    counter = 0
    while True:
        response = requests.get(url,headers=headers,timeout=15)
        if response.status_code == 429:
            ounter +=1
            if counter >= 10:
                print("Too many 429 response Skipping Anime...")
                return None
            print(f"Rate limited. Waiting... ({counter}/10)")
            time.sleep(int(response.headers.get("Retry-After",10)) +1)
            continue


        response.raise_for_status()
        break

    data = response.json()
    studio_names = [studio["name"] for studio in data["data"]["studios"]]
    genre_names = [genre["name"] for genre in data["data"]["genres"]]
    theme_names = [theme["name"] for theme in data["data"]["themes"]]
    demographics = [demographic["name"] for demographic in data["data"]["demographics"]]
    anime= {
            "mal_id": data["data"]["mal_id"],
            "main_title": data["data"]["title"],
            "english_title": data["data"]["title_english"],
            "score": data["data"]["score"],
            "episodes": data["data"]["episodes"],
            "airing_status": data["data"]["status"],
            "studio_name": studio_names,
            "genres": genre_names,
            "type" : data["data"]["type"],
            "themes" : theme_names,
            "score_votes": data["data"]["scored_by"],
            "approved" : data["data"]["approved"],
            "demographics": demographics,
            "favorites" : data["data"]["favorites"],
            "duration" : data["data"]["duration"],
            "year" :  data["data"]["year"],
            "synopsis": data["data"]["synopsis"]

        }
    

    return anime



def get_anime_id():
    url = f'https://api.tenrai.org/v1/anime/ids' 
    params = {
        "type" : ["tv","movie","ova","special","ona","tv_special"]
    }
    headers = {'X-Server-Key': API_KEY}

    response = requests.get(url,headers=headers, params=params ,timeout=15)
    response.raise_for_status()
    data = response.json()

    with open("MAL_ID_LIST.json","w") as f:
        json.dump(data,f,indent=4)


    return data








if __name__ == "__main__":

    anime_info_list = []
    mal_ids = [52991, 61987, 61440]
    for mal_id in mal_ids:
        anime_info_list.append(Scraper_Tenrai(mal_id))

    

    with open("Anime_info.json","w") as f:
        json.dump(anime_info_list,f,indent=4)


