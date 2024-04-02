import requests
from selectolax.parser import HTMLParser
from urllib.parse import unquote
import json
from datetime import datetime

site = 'https://www.avito.ru'


def get_json(url):
    """
    Функция скачивает JSON с AVITO по заданному url
    :param url:
    """
    respons = requests.get(url=url)
    print(respons.status_code)
    html = respons.text
    data = {}
    try:
        tree = HTMLParser(html)
        scripts = tree.css('script')
        for script in scripts:
            if 'window.__initialData__ ' in script.text():
                jsontext = script.text().split(';')[0].split('=')[-1].strip()
                jsontext = unquote(jsontext)
                jsontext = jsontext[1:-1]
                data = json.loads(jsontext)
                # print(jsontext)

                with open('avito_car.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False)
                print('Файл ')

    except Exception as er:
        print(er, 'Ошибка')
        return data


def get_offers(data):
    offers = []
    for key in data:
        if 'single-page' in key:
            items = data[key]['data']['catalog']['items']
            for item in items:
                if item.get('id'):
                    offer = {}
                    offer[id] = item['id']
                    offer["price"] = item['priceDetailed']['value']
                    offer["location"] = item['addressDetailed']['locationName']
                    offer["title"] = item['title']
                    offer["url"] = site + item['urlPath']
                    timestamp = datetime.fromtimestamp(item['sortTimeStamp'] / 1000)
                    timestamp = datetime.strftime(timestamp, '%d.%m.%y. в %H:%M')
                    offer["offer_time"] = timestamp
                    offers.append(offer)

    return offers


def main():
    # url = 'https://www.avito.ru/samara/avtomobili?cd=1&radius=100'
    # data = get_json(url)
    # offers = get_offers(data)
    # for offer in offers:
    #     print(offer)



    with open('avito_car.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        offers = get_offers(data)
        number = 0
        for offer in offers:
            number += 1
            print(number, offer)


if __name__ == '__main__':
    main()
