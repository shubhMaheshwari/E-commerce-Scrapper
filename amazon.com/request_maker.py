from lxml import html 
import json 
import requests
from requests.exceptions import ConnectionError
from time import sleep
import random
from fake_useragent import UserAgent


from helper import *

Trials = 5 				# Max trials to a page

# Load proxy ips and false headers to spoof the server
ua = UserAgent()
pr = open('../proxies.json','r')
proxies = json.loads(pr.read())



def request_page(url):
	for trials in range(Trials):
		try:				# runs for every trial
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
				continue

			except ValueError as e:
				print("ValueError:",e)
				continue	
			except  Exception as e:
				print("Exception:",e)
				pass	
			

			parser = html.fromstring(page.content) # Parse data to lxml
			
			XPATH_COUNT = '//h1[@id="s-result-count"]//text()'

			raw_count = parser.xpath(XPATH_COUNT)
			try:
				COUNT =  (raw_count[0].split())[0].split('-')
			except Exception as e:
				# print(e)
				# print(parser.xpath("//text()"))
				continue

			data_block = []

			# Each page has 48 items. Run the loop to scrape 

			for i in range(int(COUNT[0].replace(',',''))-1,int(COUNT[1].replace(',',''))):
				XPATH = '//li[@id="result_' + str(i) + '"]'
				data = {}

				data['ID'] = i	

				# using lxml we parse the data
				# the helper functions used here are defined in helper.py
				data['ASIN'] = get_ASIN(parser,XPATH)

				data['Name'] = get_name(parser,XPATH)

				data['Price'] = get_price(parser,XPATH)
							
				data['STARS'] = get_star(parser, XPATH)

				# Special case for a anomaly case
				data['Price'],data['REVIEWS'] = get_reviews(parser, XPATH, data['Price'])

				data_block.append(data)				

			return data_block

		except Exception as e:
			print("Detected as bot:",e)	

	print("error : failed to process the page:",url);
	return []	