import xml.etree.ElementTree as ET
import json

#Sets the path to the XML file and parses it
tree = ET.parse("animelist_1793741655_-_14096163.xml")
root = tree.getroot()

# Creates a dictionary to store the anime scores and iterates through the XML data to fill it
anime_scores = {}
i = 0
while i < len(root)-1:
    i +=1
    if root[i][12].text == "Completed":
        anime_scores[int(root[i][0].text)] = int(root[i][9].text)
    

#prints the anime scores dictionary and saves it to a JSON file
print(anime_scores)
with open("anime_scores","w") as f:
    json.dump(anime_scores,f,indent=4)

