
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def scrape_data():

    url = 'https://www.example.com'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', src=True)
    link = None

    if script_tag is not None:
        url_script = urljoin(url, script_tag['src'])
        response_sjs = requests.get(url_script)
        response_sjs.raise_for_status()
        soup_sjs = BeautifulSoup(response_sjs.content, 'html.parser')
        link = soup_sjs.select_one('a')
        if link is not None:
            link = link.get('href')

    text = soup.select_one('p').get_text() if soup.select_one('p') else None
    print(text)
    print(link)

if __name__ == "__main__":
    scrape_data()