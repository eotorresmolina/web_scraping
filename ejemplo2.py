import requests
import json
from bs4 import BeautifulSoup


def fetch_filterlist ():
    '''
    Función que realiza un get a un url
    y devuelve datos en formato json.
    '''
    url = 'https://mfwkweb-api.clarovideo.net/services/apa/metadata?sessionKey=531eed34tvfy7b73a818a234-argentina&device_so=Chrome'

    json_data_list = {}
    
    response = requests.get(url)

    if response.status_code == 200:
        json_data_list = response.json()
        
    return json_data_list


def transform_filterlist(json_data_list):
    '''
    Función que recibe datos json/diccionario y filtra
    los paises y sus respectivos ids.
    Return: [countrie, id] 
    '''
    filter_dict = {}

    countries_id = json_data_list.get('byr_filterlist_configuration')

    filter_countries = json.loads(countries_id).keys()
    ids = json.loads(countries_id).values()

    filter_ids = [id.get('filterlist') for id in ids]

    ids = [id.split(',') for id in filter_ids]

    for (countrie, id) in zip(filter_countries, ids):
        filter_dict[countrie] = {'id': id}
    
    return filter_dict

    
def fetch():
    json_data = fetch_filterlist()
    list_data = []
    
    d_countries = transform_filterlist(json_data)
    argentina = [countrie for countrie in d_countries.keys()][1]
    ids = d_countries[argentina].get('id')
    
    for value in d_countries[argentina].get('id'):
        url = 'https://mfwkweb-api.clarovideo.net/services/content/list?quantity=50&from=0&level_id=GPS&order_way=DESC&order_id=200&filter_id={}&region={}&device_id=web&device_category=web&device_model=web&device_type=web&device_so=Chrome&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.92&region={}&HKS=at6pjkq6ejfjsk8ijchfflu031'.format(int(value), argentina, argentina)
        response = requests.get(url)
        if response.status_code == 200:
            list_data.append(response.json())
    
    return argentina, ids, list_data


def transform(countrie, ids, data):

    filtered_id_film = []
    d_data= {countrie: {'filtered_film': []}}

    for (i, j) in zip(data, ids):
        for k in i.get("response").get('groups'):
            filtered_id_film.append(k.get('id'))



        d_data.get(countrie)['filtered_film'].append(j)
        index = d_data.get(countrie)['filtered_film'].index(j)
        d_data.get(countrie)['filtered_film'][index] = {j: {'id_film': filtered_id_film}}

        print(json.dumps(d_data, indent=4))

    return d_data


def get_summary(countrie, d_data):

    d_data[countrie].get('id_film')

    url = 'https://mfwkweb-api.clarovideo.net/services/content/data?device_id=web&device_category=web&device_model=web&device_type=web&device_so=Chrome&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.92&region=argentina&HKS=at6pjkq6ejfjsk8ijchfflu031&group_id={}'.format(id)
    
    response = requests.get(url)
    if response.status_code == 200:
        pass





if __name__ == '__main__':

    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'

    url = 'https://mfwkweb-api.clarovideo.net/services/content/list?quantity=50&from=0&level_id=GPS&order_way=DESC&order_id=200&filter_id=6767&region=argentina&device_id=web&device_category=web&device_model=web&device_type=web&device_so=Chrome&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.92&region=argentina&HKS=at6pjkq6ejfjsk8ijchfflu031'

    # response = requests.get(url)

    # soup = BeautifulSoup(response.content, 'html.parser')

    # result = soup.find_all('div',  class_='slider jcarousel')

    # url2 = 'https://mfwkweb-api.clarovideo.net/services/content/data?device_id=web&device_category=web&device_model=web&device_type=web&device_so=Chrome&format=json&device_manufacturer=generic&authpn=webclient&authpt=tfg1h3j4k6fd7&api_version=v5.92&region=argentina&HKS=at6pjkq6ejfjsk8ijchfflu031&group_id=927711'




    #list_data_json = fetch_filterlist()

    #filter_list = transform_filterlist(list_data_json)

    #print('\n\n',filter_list)

    countrie, ids, data = fetch()

    json_data = transform(countrie, ids, data)

    print('\n\n', json_data)