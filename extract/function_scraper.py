from bs4 import BeautifulSoup
import requests

HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', \
            'Accept-Language': 'en-US, en;q=0.5'})

def from_name_to_web_ref(popular_coin=True):
    URL = 'https://www.coingecko.com/en'
    response = requests.get(URL,headers=HEADERS)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    web_nav = soup.find('nav', {'class': 'pagy-bootstrap-nav'}).find('ul').find_all('li', {'class': 'page-item'})
    last_webpage = int(web_nav[-2].get_text())
    web_table = soup.find('table', {'class': 'table-scrollable'}).find('tbody').find_all('tr')
    dict_name = {}
    for row in web_table:
        name1 = row.find('a', {'class': 'tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between'}).get_text().strip('\n')
        name2 = row.find('a',{'class':'d-lg-none font-bold'}).get_text().strip('\n')
        web_ref = row.find('a', {'class': 'tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between'}).get('href')
        dict_name[name1] = web_ref
        dict_name[name2] = web_ref
    if popular_coin==True:
        return dict_name
    else:
        website_next='https://www.coingecko.com/en?page={}'
        for page in range(2,last_webpage+1):
            response=requests.get(website_next.format(page))
            soup=BeautifulSoup(response.content, 'html.parser')
            web_table=soup.find('table', {'class': 'table-scrollable'}).find('tbody').find_all('tr')
            for row in web_table:
                name1 = row.find('a', {'class': 'tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between'}).get_text().strip('\n')
                name2 = row.find('a', {'class': 'd-lg-none font-bold'}).get_text().strip('\n')
                web_ref = row.find('a', {'class': 'tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between'}).get('href')
                dict_name[name1] = web_ref
                dict_name[name2] = web_ref
        return dict_name

dict_dict=from_name_to_web_ref()
print(dict_dict)