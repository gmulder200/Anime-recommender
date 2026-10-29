import requests
import json

def Scraper_Jikan(Mal_ID):

    url = f'https://api.tenrai.org/v1/anime/{Mal_ID}/full'

    response = requests.get(url, timeout=15)
    print(response.status_code)
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
    


    response.raise_for_status()

    return anime



if __name__ == "__main__":

    anime_info_list = []
    mal_ids = [52991, 61987, 61440]
    for mal_id in mal_ids:
        anime_info_list.append(Scraper_Jikan(mal_id))

    

    with open("Anime_info.json","w") as f:
        json.dump(anime_info_list,f,indent=4)


