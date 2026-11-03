import xml.etree.ElementTree as ET
import json

tree = ET.parse("C:/Users/gmuld/Bureaublad/Anime Recommender/animelist_1793741655_-_14096163.xml")

root = tree.getroot()
print(root[0][0].text)


anime_scores = {}
i = 0
while i < len(root)-1:
    i +=1
    if root[i][12].text == "Completed":
        anime_scores[int(root[i][0].text)] = int(root[i][9].text)
    

   
print(anime_scores)
with open("anime_scores","w") as f:
    json.dump(anime_scores,f,indent=4)

