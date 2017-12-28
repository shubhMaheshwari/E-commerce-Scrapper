from lxml import html 
import json 
import requests
from requests.exceptions import ConnectionError
from time import sleep
import random
from fake_useragent import UserAgent



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

			# Each page has 60 items. Run the loop to get their id 
			try:
				DATA = parser.xpath('//script[contains(text(),"window.pageData")]//text()')[0]
				DATA = json.loads(DATA.replace('window.pageData=','')) 
		
			except Exception as e:
				print("Error:",e)
				continue

			data_block = DATA['mods']['listItems']

			if data_block == []:
				return [],False

			# Scrape data from each object
			return data_block,True

		except Exception as e:
			print("Error due to:",e)	

	print("error : failed to process the page:",url);
	return [],True