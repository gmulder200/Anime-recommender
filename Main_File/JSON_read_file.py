import json



with open("anime_info_list.json","r") as f:
        data=json.load(f)

    print(data)
