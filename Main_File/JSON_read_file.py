import json


if __name__ == "__main__":
        
    with open("anime_info_list.json","r") as f:
        data=json.load(f)

    print(len(data))

    for anime in data:
        if anime["score"] >= 8.0 and anime["approved"]:
            print(anime["main_title"])


