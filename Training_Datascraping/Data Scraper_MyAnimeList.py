
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def scrape_data():

    #url = 'https://myanimelist.net/anime/52991/Sousou_no_Frieren?q=fieren&cat=anime'
    #url = 'https://myanimelist.net/anime/61967/Black_Clover_2nd_Season'
    url = 'https://myanimelist.net/anime/61316/Re_Zero_kara_Hajimeru_Isekai_Seikatsu_4th_Season'

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    Main_title = soup.find('h1',class_='title-name')
    main_title = Main_title.get_text(strip=True) if Main_title else None
    Title_english = soup.find('p', class_='title-english') 
    Score = soup.find('div', class_='score-label')
    Episodes = soup.find('span', string='Episodes:').next_sibling.strip()
    Airing = soup.find('span', string='Status:').next_sibling.strip()
    Studio = soup.find('span', string='Studios:')
    Studio_name = Studio.find_next('a') if Studio else None
    Genres = soup.find('span', string='Genres:')
    Genre_parent = Genres.find_parent('div') if Genres else None
    Genres_list = [genre.text for genre in Genre_parent.find_all('a')] if Genre_parent else []
    Mal_ID = url.split('/')[4]

    anime= {
        "mal_id": Mal_ID,
        "main_title": main_title if main_title else None ,
        "english_title": Title_english.text if Title_english else None,
        "score": Score.text if Score else None,
        "episodes": Episodes,
        "currently_airing": Airing,
        "studio_name": Studio_name.text if Studio_name else None,
        "genres": Genres_list 
    }

    return(anime)

if __name__ == "__main__":
    print(scrape_data())