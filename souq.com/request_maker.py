from lxml import html 
import json 
import requests
from requests.exceptions import ConnectionError
from time import sleep
import random
from fake_useragent import UserAgent


from helper import *

Trials = 10 				# Max trials to a page

# Load proxy ips and false headers to spoof the server
ua = UserAgent()
pr = open('../proxies.json','r')
proxies = json.loads(pr.read())

def get_page(url):
	try:			# runs for every proxy added
		try:		# runs for successful addition of proxy

			# Choose a random proxy network

			proxy = random.sample(proxies,1)[0]
			proxyDict = { 
						"http"  : "http://" + proxy['ip'] + ':' + proxy['port'] , 
						"https" : "https://" + proxy['ip'] + ':' + proxy['port'], 
						"ftp"   : "ftp://" + proxy['ip'] + ':' + proxy['port']}
		except:
			proxyDict = None
		headers = {'User-Agent' : ua.random}
		
		# Make a request to the given url

		page = requests.get(url, headers=headers,  proxies=proxyDict,timeout=8)
		print("Extracting:",url)
		sleep(2)

	except ConnectionError as c:
		try:
			proxies.remove(proxy)				
		except:
			pass
		return None

	except ValueError as e:
		print("ValueError:",e)
		return None	
	except  Exception as e:
		print("Exception:",e)
		return None

	return page

def request_page(url):
	for trials in range(Trials):
		try:				# runs for every trial
				
			page = get_page(url)

			if page == None:
				continue

			parser = html.fromstring(page.content) # Parse data to lxml

			# Check whether the given page is in the limit of the data provided by the site
			item_limit = parser.xpath('//li[@class="total"]//text()')
			if item_limit == []:
				return [],False

			# Each page has 60 items. Run the loop to get their id 
			XPATH = '//div[@class="column column-block block-grid-large single-item"]'

			X_ID = XPATH + '/@data-ean'
			ID = parser.xpath(X_ID)
			if ID  == []:
				print(page.content)
				continue

			

			data_block = []

			# Scrape data from each object
			for x in ID:
				data = {}

				data['ID'] = x	
				X_ITEM = XPATH + '[@data-ean=' + str(x) + ']'

				# using lxml we parse the data
				# the helper functions used here are defined in helper.py
				data['Name'] = get_name(parser,X_ITEM)
				data['Brand-Name'] = get_brand_name(parser,X_ITEM)
				data['Category-Name'] = get_category_name(parser,X_ITEM)

				data['Price(AED)'] = get_price(parser,X_ITEM)
				data['Real-Price(AED)'], data['Discount(%)'] = get_real_price(parser,X_ITEM,data['Price(AED)'])
				data['STARS(%)'] = get_star(parser, X_ITEM)
				data['Free Shipping'] = get_shipping(parser,X_ITEM)

				data_block.append(data)				

			return data_block,True

		except Exception as e:
			print("Error due to:",e)	

	print("error : failed to process the page:",url);
	return [],True