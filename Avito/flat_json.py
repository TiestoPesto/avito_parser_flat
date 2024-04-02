import requests
import sqlite3
from datetime import datetime


def get_offer(item):
	offer = {}
	
	# title = item['title'].split(', ')
	timestamp = datetime.fromtimestamp(item['time'])
	timestamp = datetime.strftime(timestamp, '%d.%m.%y. в %H:%M')
	
	offer['offer_id'] = item['id']
	offer['title'] = item['title']
	offer['price'] = item['price']
	offer['price_metr'] = item['normalizedPrice']
	offer['district'] = item['location']
	offer['address'] = item['address']
	offer['offer_time'] = timestamp
	offer['url'] = 'https://www.avito.ru' + item['uri_mweb']
	
	return offer


def check_database(item):
	offer_id = item['id']
	with sqlite3.connect('flat_samara.db') as connection:
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
		                VALUES (NULL, :offer_id, :title, :price, :price_metr, :district, :address, :offer_time, :url)
		            """, offer)
			connection.commit()
			print(f'Объявление {offer_id} добавлено в базу данных')


def get_offers(data):
	items = data['result']['items']
	for item in items:
		if 'item' in item['type']:
			check_database(item['value'])


# получаем JSON с Авито мобильной версии
def get_json():
	# cookies = {
	# 	'u': '2xsvjemx.uhpy75.9igcadomv8w0',
	# 	'_gcl_au': '1.1.1084298413.1678295861',
	# 	'_ga': 'GA1.1.1954345358.1678295862',
	# 	'tmr_lvid': '975267ee5e1fa66accc62a2b14dabd82',
	# 	'tmr_lvidTS': '1678295862450',
	# 	'adrdel': '1',
	# 	'adrcid': 'AKZ9GiWyuClwx7MmQx53LIw',
	# 	'uxs_uid': '23504420-bdd5-11ed-9df6-c5b8744b8120',
	# 	'_ym_uid': '1678295864635958333',
	# 	'_ym_d': '1678295864',
	# 	'_ym_isad': '2',
	# 	'f': '5.e3d69e1fd90b3b452cc52874d9fb7711171cd3c73f634687171cd3c73f634687171cd3c73f634687171cd3c73f634687171cd3c73f634687171cd3c73f634687171cd3c73f634687171cd3c73f634687cec4d980e289734f1173aa12b46ae7920df103df0c26013a8b1472fe2f9ba6b90df103df0c26013a0df103df0c26013adc5322845a0cba1aa2d6277e27462e9f9369d542f7ef95b3ad59ae6628fbf800915ac1de0d034112dc0d86d9e44006d8143114829cf33ca7143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fad99271d186dc1cd0b5b87f59517a23f2c772035eab81f5e1c772035eab81f5e1c772035eab81f5e1c772035eab81f5e1143114829cf33ca7bed76bde8afb15d28e3a80a29e104a6c2c61f4550df136d8bd97c9ffbeaa92ba7241224a7d6c09dc021dce8db01be7bff4533f10341e9ac0df9a46b4897084f529aa4cecca288d6b8eeeca001a5ea5dbe31784d6ce1af7c746b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7ac304d925f42244dcc74dccca02b6edffe2da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b53778cee096b7b985bf37df0d1894b088',
	# 	'ft': '"0bxVRbh2dMEXRPRuUUZLoujy213QPgfe0YdkyXKj7nMcxPGJ2c2gKwiTe5jO/TMsLv7eOk6GOtSXYuY55JH+2O9H3/RtsOh0y214GBfLMrK09vpLoqQnvleSFWa7bqwLFzCs58tNKpxO6c4nTFn/ACBaIyxeH65Gb0EQeKW2qjmVNuoRxCm+7F9pcNu5q4xL"',
	# 	'redirectMav': '1',
	# 	'_mlocation': '637640',
	# 	'_mlocation_mode': 'laas',
	# 	'isCriteoSetNew': 'true',
	# 	'tmr_detect': '0%7C1678296618997',
	# 	'_buzz_fpc': 'JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi5tLmF2aXRvLnJ1JTIyJTJDJTIyZXhwaXJlcyUyMiUzQSUyMkZyaSUyQyUyMDA4JTIwTWFyJTIwMjAyNCUyMDE3JTNBMzAlM0EyNiUyMEdNVCUyMiUyQyUyMlNhbWVTaXRlJTIyJTNBJTIyTGF4JTIyJTJDJTIydmFsdWUlMjIlM0ElMjIlN0IlNUMlMjJ2YWx1ZSU1QyUyMiUzQSU1QyUyMjRhM2NjYTY4YWRiNGVhMjk3MzViMDRmZjMyMjdjZjYwJTVDJTIyJTJDJTVDJTIyZnBqc0Zvcm1hdCU1QyUyMiUzQXRydWUlN0QlMjIlN0Q=',
	# 	'_inlines_order': 'params[549].params[578].params[2950].params[110486].params[1459].params[110688].params[121749].params[120711].params[120712].params[498].categoryNodes.locationGroup.params[2952]',
	# 	'v': '1678303839',
	# 	'buyer_laas_location': '653040',
	# 	'_ym_visorc': 'b',
	# 	'gMltIuegZN2COuSe': 'EOFGWsm50bhh17prLqaIgdir1V0kgrvN',
	# 	'dfp_group': '62',
	# 	'cto_bundle': 'Nzjv8l9nZWI2NzZ4TFdNMnJJSW9IS3hwOTJHaUJrM3pBMEt1VkFQZGgwZXplQkdBc0NwUkVRZnVoZnhNaVJRUDBOMm80YXhnTW1NV09IY1dMQWkzVHZoZ29JYXhDRUk3N0lPVkZNRyUyQlJpRHNrdGRBbmglMkJ4Y1N5WEhFS2M2ZmVUNnVnUGxXanpkSTZTYlpNWUk4T3FIajhRRG5nJTNEJTNE',
	# 	'_ga_M29JC28873': 'GS1.1.1678303848.2.1.1678304551.60.0.0',
	# 	'luri': 'permskiy_kray',
	# 	'buyer_location_id': '643700',
	# 	'sx': 'H4sIAAAAAAAC%2F5zTS7LiPAwF4L1kzMC2ZD16N7ZkB5IbGu5PwqOLvf%2FFgK5mejfw1SkdnT9DylVT1RqrcBaR3FpN0muKzSr1OPz6M2zDr%2BE%2BI8MCC934nL6XcU%2FHctNyF18O3HjYDW34FYkFNGiOz92AJLGyd9CcU8fkNeeUJadssVCyt5zGdYwyMspjWpCs9HjH7bjv53S54eMfWVIieO6GjGANPVaI4sF6sNoBUFqVKNnxLa8HCphOcjT9796%2FRlgSXDS2o21bP18%2FMieUl1wzIKYcqxmxJsCgRt5UWhaM%2BpZFxrCeN5qX441wO0C0cJ41mobrHj6vwarP3UBEZM7UlTQTkjauDdQ5BzP2v%2FLvrz3iva5bPVy%2BOV1ORwrhdj1M6zqZ58%2FMObzkIuis2lLFGrzkoKEhZ%2FAoLI1%2F0qBwfu4GNsIO3RhMO2JIDhY0cAbBApzeMn%2Fd58v9ez5D77ft91Tm5SpfJyzZp1NuHw1CxuduEGoaU0arNYaWPWFJHqwUV4se6ls%2BjePxItdTjH66ar%2BsUzkcJ%2BbLMtFpCZ%2FXoPSSu5hFIMyVkWrskIrn2oH5lR9%2FJOdXg4otEjsR9AgeHWpzaTEE19ILyFseZwxruxPDPTU8Py4hr3EFpf18Oqz4uRR9LaXGROZCmLpRDgrM7KjNHGIvbD%2FJDPD6DSsxNuYeWFNAbSrKvXijbCkJ%2Fr2GHza9PfaH7TLKgrc5TI%2F9OOY5TOsy76d%2FG4QQX0vplY1i9ZqakEM1l%2BbNxTGzRbMffR3l5%2FP%2FAAAA%2F%2F%2FpNpgDkwQAAA%3D%3D',
	# }
	#
	# headers = {
	# 	'authority': 'm.avito.ru',
	# 	'accept': 'application/json, text/plain, */*',
	# 	'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
	# 	'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
	# 	'content-type': 'application/json;charset=utf-8',
	# 	'referer': 'https://m.avito.ru/samara/kvartiry/prodam-ASgBAgICAUSSA8YQ?district=801-796-798-800-795-799&f=ASgBAQECBkSSA8YQ5hYCrL4NAsDBDbr9N47eDgKQ3g4CA0DkB0T4UfxR_lGW65kCygg0_liAWYJZqu4OJMih4wLKoeMCA0WECRN7ImZyb20iOjI3LCJ0byI6NzB9jC4UeyJmcm9tIjozLCJ0byI6bnVsbH2QLhV7ImZyb20iOjE1LCJ0byI6bnVsbH0&radius=0&s=104&presentationType=serp&searchForm=true',
	# 	'sec-ch-ua': '"Opera";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
	# 	'sec-ch-ua-mobile': '?1',
	# 	'sec-ch-ua-platform': '"Android"',
	# 	'sec-fetch-dest': 'empty',
	# 	'sec-fetch-mode': 'cors',
	# 	'sec-fetch-site': 'same-origin',
	# 	'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko)'
	# 	              ' Chrome/90.0.4430.91 Mobile Safari/537.36',
	# }
	#
	# response = requests.get(
	# 	'https://m.avito.ru/api/11/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=653040&districtId[]=801&districtId[]=796&districtId[]=798&districtId[]=800&districtId[]=795&districtId[]=799&categoryId=24&params[201]=1059&params[549][]=5695&params[549][]=5696&params[549][]=5697&params[578-from-int]=27&params[578-to-int]=70&params[2950-from-int]=3&params[110486]=1&params[1459]=1&params[110688][]=458589&params[121749][]=2910308&params[121749][]=2910309&params[120711]=1&params[120712]=1&params[498][]=5244&params[498][]=5246&params[498][]=5247&params[498][]=2308811&params[2952-from-int]=15&sort=date&presentationType=serp&countOnly=1',
	# 	cookies=cookies,
	# 	headers=headers,
	# )
	
	cookies = {
		'gMltIuegZN2COuSe': 'EOFGWsm50bhh17prLqaIgdir1V0kgrvN',
		'u': '2xsxxj9n.uhq3gi.15hx92on9tew0',
		'buyer_laas_location': '653040',
		'luri': 'samara',
		'buyer_location_id': '653040',
		'_gcl_au': '1.1.1624442268.1678647719',
		'_ga': 'GA1.1.2003958592.1678647719',
		'_ym_uid': '167864772092855662',
		'_ym_d': '1678647720',
		'_ym_isad': '2',
		'v': '1678649544',
		'sx': 'H4sIAAAAAAAC%2FwTAMQ7CMAwF0Lv8mYHS%2BBvnODiOogxIlOKBqnfvO0CS3pTdaMJCC33Fak3l7q7NUA8kKuYYe7rPx6dvuy%2Fff0%2BTbbbxkwy%2BcUOgLtSnrmKlnOcVAAD%2F%2F%2FzMeFNbAAAA',
		'f': '5.673c10cb09ba31f3cc0065cb1b69001fb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0c02c2f5f4b9c76ee47e7721a3e5d3cdbb46b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8b175a5db148b56e9bcc8809df8ce07f640e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0ac2ebf3cb6fd35a0ac0df103df0c26013a7b0d53c7afc06d0bba0ac8037e2b74f92da10fb74cac1eab71e7cb57bbcb8e0f71e7cb57bbcb8e0f71e7cb57bbcb8e0f0df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686adbf5c86bc0685a4ff42a08f76f4956e8502c730c0109b9fbb3fe55cf167ea7c4337ca2f19b516c45029aa4cecca288d6b8eeeca001a5ea5dbe31784d6ce1af7c746b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7ac304d925f42244dcce1e4560e9472c8a62da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b53778cee096b7b985bf37df0d1894b088',
		'ft': '"tbnS490pHLDE3rsEodjRcwPSeFy0kXyml9zsRV0DGPWut9SkAd9HlI3w9oA6vpxWQg+TQmc2+eVzD9TrJUpMb9WXryNMiWJmTt6Mx3c4GNu3I3N+zjr1SW0mBcszsEh6km9stfnr5/N4J8HwWfG2TOh9IEcm3hOZUlb7FTKvbKl7UT1JHgOGx6lPqAvZM6Ho"',
		'_ym_visorc': 'b',
		'uxs_uid': 'a0bd9220-c10c-11ed-8174-6f38255c35a4',
		'redirectMav': '1',
		'_mlocation': '621540',
		'_mlocation_mode': 'default',
		'_ga_M29JC28873': 'GS1.1.1678649547.2.1.1678650015.53.0.0',
		'_inlines_order': 'categoryNodes.locationGroup.params[549].params[578].params[2950].params[110486].params[1459].params[110688].params[498]',
	}
	
	headers = {
		'authority': 'm.avito.ru',
		'accept': 'application/json, text/plain, */*',
		'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
		'content-type': 'application/json;charset=utf-8',
		'cookie': 'gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; u=2xsxxj9n.uhq3gi.15hx92on9tew0; buyer_laas_location=653040; luri=samara; buyer_location_id=653040; _gcl_au=1.1.1624442268.1678647719; _ga=GA1.1.2003958592.1678647719; _ym_uid=167864772092855662; _ym_d=1678647720; _ym_isad=2; v=1678649544; sx=H4sIAAAAAAAC%2FwTAMQ7CMAwF0Lv8mYHS%2BBvnODiOogxIlOKBqnfvO0CS3pTdaMJCC33Fak3l7q7NUA8kKuYYe7rPx6dvuy%2Fff0%2BTbbbxkwy%2BcUOgLtSnrmKlnOcVAAD%2F%2F%2FzMeFNbAAAA; f=5.673c10cb09ba31f3cc0065cb1b69001fb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0cb456d7c4b56f6c0c02c2f5f4b9c76ee47e7721a3e5d3cdbb46b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8b175a5db148b56e9bcc8809df8ce07f640e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0ac2ebf3cb6fd35a0ac0df103df0c26013a7b0d53c7afc06d0bba0ac8037e2b74f92da10fb74cac1eab71e7cb57bbcb8e0f71e7cb57bbcb8e0f71e7cb57bbcb8e0f0df103df0c26013a037e1fbb3ea05095de87ad3b397f946b4c41e97fe93686adbf5c86bc0685a4ff42a08f76f4956e8502c730c0109b9fbb3fe55cf167ea7c4337ca2f19b516c45029aa4cecca288d6b8eeeca001a5ea5dbe31784d6ce1af7c746b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7ac304d925f42244dcce1e4560e9472c8a62da10fb74cac1eab2da10fb74cac1eab25037f810d2d41a8134ecdeb26beb8b53778cee096b7b985bf37df0d1894b088; ft="tbnS490pHLDE3rsEodjRcwPSeFy0kXyml9zsRV0DGPWut9SkAd9HlI3w9oA6vpxWQg+TQmc2+eVzD9TrJUpMb9WXryNMiWJmTt6Mx3c4GNu3I3N+zjr1SW0mBcszsEh6km9stfnr5/N4J8HwWfG2TOh9IEcm3hOZUlb7FTKvbKl7UT1JHgOGx6lPqAvZM6Ho"; _ym_visorc=b; uxs_uid=a0bd9220-c10c-11ed-8174-6f38255c35a4; redirectMav=1; _mlocation=621540; _mlocation_mode=default; _ga_M29JC28873=GS1.1.1678649547.2.1.1678650015.53.0.0; _inlines_order=categoryNodes.locationGroup.params[549].params[578].params[2950].params[110486].params[1459].params[110688].params[498]',
		'referer': 'https://m.avito.ru/items/search?locationId=653040&localPriority=0&footWalkingMetro=0&categoryId=24&params[201]=1059&params[549][]=5695&params[549][]=5696&params[549][]=5697&params[144532]=1&params[578-from-int]=27&params[578-to-int]=70&params[2950-from-int]=3&params[110486]=1&params[1459]=1&params[110688]=458589&params[2710-from-int]=8&params[498][]=5244&params[498][]=5246&params[498][]=5247&params[498][]=2308811&sort=date&presentationType=serp',
		'sec-ch-ua': '"Opera";v="95", "Chromium";v="109", "Not;A=Brand";v="24"',
		'sec-ch-ua-mobile': '?1',
		'sec-ch-ua-platform': '"Android"',
		'sec-fetch-dest': 'empty',
		'sec-fetch-mode': 'cors',
		'sec-fetch-site': 'same-origin',
		'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36',
		'x-laas-timezone': 'Asia/Baku',
	}
	
	response = requests.get(
		'https://m.avito.ru/api/11/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=653040&localPriority=0&footWalkingMetro=0&categoryId=24&params[201]=1059&params[549][]=5695&params[549][]=5696&params[549][]=5697&params[144532]=1&params[578-from-int]=27&params[578-to-int]=70&params[2950-from-int]=3&params[110486]=1&params[1459]=1&params[110688]=458589&params[2710-from-int]=8&params[498][]=5244&params[498][]=5246&params[498][]=5247&params[498][]=2308811&sort=date&page=1&lastStamp=1678650000&display=list&limit=25&presentationType=serp',
		cookies=cookies,
		headers=headers,
	)
	
	data = response.json()
	print(data)


# return data


def main():
	data = get_json()


# get_offers(data)


if __name__ == '__main__':
	main()
