Author :
Gertjan Mulder 

Project Goal :
Create a personal anime recommender which given an input of a myanimelist.net animelist recommends a certain amount of anime according the recommender.

Files :
AnimeListImport.py
    - Import the animelist which is located on the computer (can be downloaded on the myanimelist site) and loops through the anime_ID and scores which are then put into a .json File

JSON_read_file.py (Outdated)
    -Outdaded file to read .json files with.

main.py
    - Main File to run created functions in. Later will be used as main function where functions required for the programm will be called an ran.

SQLite_Db.py
    - File which controls the SQLite Database. In this file multiple function are created to add, search or create the database.

Tenrai_API_Animedata.py
    - File which controls the import of the animedata from the Tenrai API. Consists of 2 functions one which fetches anime data when given a anime ID. The other fetches all available anime ID within the given parameters.

