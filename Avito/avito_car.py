"""
Подключаем к парсеру Авито Базу данных
И парсим новым быстрым способом
Парсер каждую минуту заходит на площадку и собирает объявление
Проверяет наличие сообещния в БД, если его нет, то дополняет БД
"""
import sqlite3
import requests
from datetime import datetime

def create_db(name):
    connection = sqlite3.connect(f'data_base/{name}.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE offers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            offer_id INTEGER,
            title TEXT,
            price INTEGER,
            address TEXT,
            time TEXT,
            url TEXT
        )
    """)
    connection.close()

def get_json():
    headers = {
        'authority': 'm.avito.ru',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36',
        'content-type': 'application/json;charset=utf-8',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://m.avito.ru/items/search?categoryId=9&locationId=653040&radius=100&localPriority=1&sort=date&isGeoProps=true&presentationType=serp',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'u=2t5r8o9c.qbz1ua.1ddkcap1qze00; v=1643883096; luri=samara; buyer_location_id=653040; sx=H4sIAAAAAAAC%2FwTASQ7DIAwF0Lv8dRd2sMxwG%2Bw0HTapKhVREHfPmyA2T7rXKIeSkQmbBzt2jeJOnlAmGgp86%2BM7LPrz34TOcL575Yf8Xlvlnj644Y7CKiFrlqxrXQEAAP%2F%2FIJc%2BZ1sAAAA%3D; dfp_group=52; _gcl_au=1.1.1999868645.1643883100; _ym_uid=1643883100529165980; _ym_d=1643883100; _gid=GA1.2.1465687868.1643883100; _ym_visorc=b; tmr_lvid=47d51dbd0b4f544733f1e530960eb617; tmr_lvidTS=1643883100511; _ym_isad=2; f=5.df155a60305e515acc0065cb1b69001fb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0c02c2f5f4b9c76ee47e7721a3e5d3cdbb46b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8b175a5db148b56e9bcc8809df8ce07f640e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0acf722fe85c94f7d0c0df103df0c26013a7b0d53c7afc06d0bba0ac8037e2b74f92da10fb74cac1eab71e7cb57bbcb8e0f71e7cb57bbcb8e0f2da10fb74cac1eab0df103df0c26013a93e76904ac7560d304dab5ef1a68b40d870473681516ef3f674d3299cca3d4bbc91376f4301c077f2985db2d99140e2d50c4efa1efd7c36f0fd50f4c86b8841238adc93de73b65bab72af306cd38b63d2da10fb74cac1eab0df103df0c26013a0df103df0c26013aafbc9dcfc006bed904a09f60eb2fff05682c59c6c4d925c23de19da9ed218fe23de19da9ed218fe2d6fdecb021a45a31b3d22f8710f7c4ed78a492ecab7d2b7f; ft="xbb+Pwa83Fza639xHeHZCDVbNc6iX90SkfS/3HlF5o9Q5rMof4R2VW+AHa94ZkNWOsAW6K5TLSabqkm8e7KDUyaIJYjd2JrqU0RC4E0OkbOYoM/NiHEqGQ9uJZHpoWKOlGe0pJVQ9fQMCKw2U67OnssD1oKokoZy/2kCwhqc6Ve/UQl5khHzZ5A6Bx5ar8+n"; _mlocation=621540; _mlocation_mode=default; _dc_gtm_UA-2546784-1=1; _ga=GA1.1.1536054805.1643883100; cto_bundle=ZTiUvF96OVdobzJuQlpCdlczOWJvcVJoSnExRFVQSnhUNUd3VUpOYjZ2OUtaVGdCRUNIUzdkSWQlMkJNQjQyelRaRkNPeU5QdVdUdVR6ZDhadmFYZ2FQdkh6NjJud1haQmFUZjdxeExKSDlYUEE1MDY3NHpheWpUWTFaeWtDZnpaNXprcGdNMVNxQXBXRWZzSEJBMGRvSXFhOTVHdyUzRCUzRA; __gads=ID=fc487db1734d2dc5:T=1643883193:S=ALNI_MauUVmMUpkvJRxYqG1uGg44yWRsaw; isCriteoSetNew=true; tmr_detect=0%7C1643883194066; st=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoidko0TkJ5SlU2TElJTGRDY3VNTkdBZm5PRWwySzdtS01KZXBFMDh1VUFITFBwUWhCdmRwS3kvVldkdXhwbnNyMjl6R3BPcHZPa011V2dUNkw0S3pCU090cVhYc2NIZHQwY2h5eHdDU25UYmp3UDI5VmkxUHptOGNvV0I2RjRzYkhvdG9PUUZuVXIwYUhrUDUrLzY3QmFHdTB2RTRocE0vQlZmdlRhMG4ycWJFVnlmRDZ0YVZoaHpSVWcrS1JBTHA1Sys4NmVsVzVldWJzWjVGTGdCcHFPcW9sUDBIbHovSFMycGV4RUJkU3F1Z2RyU2tCSWUvYmFZc2tsNUx3MkpaMmkrMDVSRzl3RzRNc1lvejZvbzY0dXg1L0tKV1JUTDVkUERWWUlPNm9FTWZiSlpDcnpkMS9oRDZhT0VJNGhUeGlNdkRPNkNKMFdXOERmWFJHQXdoRy9rdm1jc09yc3liSFVPTGhjWEJTaTlSSURwa3ZnQkpaMHdTS0VDVWozdjFuUWRPMDVVQXZwNm1IS3pNZ3pNWUtxRWxQcGo0eldDbUNWN21MRFl0aVJGT1NRODRwRDZaWXM2MkU2Q1B5bis0cFVhYjkzRVdiUVhOSnZVVmdNS1VnYkNsei8vZkYvQzFnSHBkeGplUjVhNWZMdXZsWGRWNUZaUXo1UW1CcW9GQVF0RVVWOHEwbStNOFBncG9LVlV2VFM4SFJ1WlRaUHdqRlFrZ3daLy9ZUXJuYUFIYzFPUjhQM3BTa04vM2J4TU5Zb2puNFdaMERoTUtTWVBnbmRpOWFpVlpxTFJwWlNHVVlab2ltOFBZTlZwMGJvQi9rZExKc0lldm5ZTUFGaDAzOHRVNmIvWFhVQmZaaE8wZCtySC9EK3FWMEVEd01xYmVNMjlWMXhNby9XbTczRm9yZ0Mrd2lzUE5ROTluVVY4a2srWHdXTGJiT0JjY2hKMzlMSFpuR1ZTcEwvSUdyb1Y1aERIZ1JqbmJHaVY0ZG05bW9VRlpOdjR6K1BnOWpTZHpyWDF4WWJyQTVCanNmQkVSazRmcDd5ZlRFVnlEcTZNaEFQTGRUTVBVQ21hU1hMckF6cG10OFhnSm02NEp5OUNmMUZPeEJGZC9HazJXY0dESzdtVHFEVDlYS1BvZWhFcGxqaldUMDhWc2ZxbnNybFJUK0NDWVhVU28vaUJMZ3BNZ0RSRzJuVTZlR282OUpiV21icXRMby81M0lreFpJOEVGcm9EdUhLUlRVZVJJaHRXekxFU211MU96VzgyOHEydE83aFV5a1N4V1Q3ZnNHM1JTR0hrNEZBdz09IiwiaWF0IjoxNjQzODgzMTY2LCJleHAiOjE2NDUwOTI3NjZ9.2U32_qQ3U_zPDhjlpM6quHKaMK5Ywvlq4D-iYbfBntY; ST-TEST=TEST; tmr_reqNum=9; _ga_9E363E7BES=GS1.1.1643883099.1.1.1643883210.37',
    }

    params = (
        ('key', 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'),
        ('categoryId', '9'),
        ('locationId', '653040'),
        ('radius', '100'),
        ('localPriority', '1'),
        ('sort', 'date'),
        ('isGeoProps', 'true'),
        ('page', '1'),
        ('lastStamp', '1643883180'),
        ('display', 'list'),
        ('limit', '30'),
    )
    url = 'https://m.avito.ru/api/11/items'
    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)
    data = response.json()
    return data


def get_offer(item):
    offer = {}

    price = ''.join(item['price'].replace(' ₽ в месяц', '').split())
    # title = item['title'].split(', ')
    timestamp = datetime.fromtimestamp(item['time'])
    timestamp = datetime.strftime(timestamp, '%d.%m.%y. в %H:%M')

    offer['offer_id'] = item['id']
    offer['title'] = item['title']
    offer['price'] = item['price']
    # offer['market'] = item['badgeBar']
    offer['address'] = item['location']
    offer["offer_time"] = timestamp
    offer['url'] = 'https://www.avito.ru' + item['uri_mweb']

    return offer


def check_db(item):
    offer_id = item['id']
    with sqlite3.connect('avito2.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT offer_id FROM offers WHERE offer_id = (?) 
        """, (offer_id,))
        result = cursor.fetchone()
        if result is None:
            offer = get_offer(item)
            # TODO send_telegram(offer)

            cursor.execute("""
                INSERT INTO offers
                VALUES (NULL, :offer_id, :title, :price, :address, :offer_time, :url)
            """, offer)
            connection.commit()
            print(f'Объявление {offer_id} добавлено в базу данных')


def get_offers(data):
    items = data['result']['items']
    for item in items:
        if 'item' in item['type']:
            check_db(item['value'])


def main():
    name = 'new_car'
    create_db(name)
    data = get_json()
    get_offers(data)


if __name__ == '__main__':
    main()
