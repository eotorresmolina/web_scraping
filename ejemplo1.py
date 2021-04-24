# Ejemplo 1 de Web Scraping

import requests
import json
from bs4 import BeautifulSoup

def fetch_teams(url):
    teams = []
    count = 0
    max_value = 20
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('span', class_='nombre-equipo')

        for result in results:
            if count < max_value:
                teams.append(result.text)
            else:
                break
            
            count += 1

    return teams


def fetch_points (url):
    points = []
    count = 0
    max_value = 20

    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('td', class_='destacado')

        for result in results:
            if count < max_value:
                points.append(result.text)
            else:
                break

            count += 1

    return points


def transform (fetch1, fetch2):

    json_teams = [{x: y} for x, y in zip(fetch1, fetch2)]

    return json_teams



if __name__ == '__main__':
    url = 'https://resultados.as.com/resultados/futbol/primera/clasificacion/'
    
    teams = fetch_teams(url)
    points = fetch_points(url)

    print('\n', teams)
    print('\n', points)

    json_teams = transform(teams, points)

    print('\n', json.dumps(json_teams, indent=4))
