import requests

def Scraper_Jikan(Mal_ID):

    url = f'https://api.tenrai.org/v1/anime/{Mal_ID}/full'

    response = requests.get(url, timeout=15)
    print(response.status_code)
    data = response.json()
    studio_names = [studio["name"] for studio in data["data"]["studios"]]
    genre_names = [genre["name"] for genre in data["data"]["genres"]]

    anime= {
            "mal_id": data["data"]["mal_id"],
            "main_title": data["data"]["title"],
            "english_title": data["data"]["title_english"],
            "score": data["data"]["score"],
            "episodes": data["data"]["episodes"],
            "currently_airing": data["data"]["status"],
            "studio_name": studio_names,
            "genres": genre_names
        }
    


    response.raise_for_status()

    return anime



if __name__ == "__main__":

    anime_info_list = []
    mal_ids = [52991, 61987, 61440]
    for mal_id in mal_ids:
        anime_info_list.append(Scraper_Jikan(mal_id))



    print(anime_info_list)