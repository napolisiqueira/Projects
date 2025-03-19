import requests
import pandas as pd
from bs4 import BeautifulSoup
from itertools import product


DOMAIN = "path_web"
URL = f"{DOMAIN}/2025-athletes-ranking"
HEADERS = {'User-agent': 'Mozilla/5.0'}
PARAMETERS  = {
    "filters[filters]": 'ranking-geral-gi',
    "filters[Branking_category]": 'adult',
    "filters[gender]": 'male',
    "filters[belt]": 'black',
    "filters[weight]": None,
    "page": 1
}





def get_page_content(url, header, parameters):
    response = requests.get(URL, headers=HEADERS, params=PARAMETERS).text
    soup = BeautifulSoup(response,'html.parser')
    return soup

def parse_athletes(soup, kimono, category, gender, belt, division):
    table = soup.find('table')
    if not table:
        return None
    athletes = []
    rows = table.find_all('tr')
    if not rows:
        return None
    for row in rows:
        photo_cell =   row.find('td', class_ = 'photo reduced')
        name_cell = row.find('td', class_ = 'name-academy')
        point_cell = row.find('td', class_ = 'pontuantion')
        rank_cell = row.find('td', class_ =  'position')
        
        photo = photo_cell.find('img')['src']
        name_tag = name_cell.find('div', class_ = 'name').find('a')
        name = name_tag.get_text(strip=True)
        details =  name_tag['href']
        points = point_cell.get_text(strip=True)
        rank = rank_cell.get_text(strip=True)


        athlete = {
            'photo': photo,
            'name': name,
            'details': details,
            'points': points,
            'rank': rank,
            'kimono': kimono,
            'category': category,
            'gender': gender,
            'belt': belt,
            'division': division
        }
        athletes.append(athlete)
    return athletes

def list_filters(soup, filter_id):
    filters = soup.find(id = filter_id).find_all('option')
    return [item['value']for item in filters[1:]]





soup_filters = get_page_content(URL,HEADERS,PARAMETERS)
kimono = list_filters(soup_filters, 'filter_s')
category = list_filters(soup_filters, 'filter_ranking_category')
gender = list_filters(soup_filters, 'filter_gender')
belt = list_filters(soup_filters, 'filter_belt')
division = list_filters(soup_filters, 'weight_filter')





all_athletes = []


for k, c, g, b, d in product(kimono, category, gender, belt, division):
    page = 1
    while True:
        print(f"Scraping: {k}, {c}, {g}, {b}, {d} for page {page}")
        PARAMETERS['filters[s]'] = k
        PARAMETERS['filters[Branking_category]'] = c
        PARAMETERS['filters[gender]'] = g
        PARAMETERS['filters[belt]'] = b
        PARAMETERS['filters[weight]'] = d
        PARAMETERS['page'] = page
        soup_athletes =get_page_content(URL, HEADERS, PARAMETERS)
        athletes = parse_athletes(soup_athletes, k, c, g, b, d)
        if athletes is None:
            break
        all_athletes.extend(athletes)
        page+=1

df_athletes = pd.json_normalize(all_athletes)
df_athletes
df_athletes.to_excel('WebScrapingResult.xlsx', index=False)
