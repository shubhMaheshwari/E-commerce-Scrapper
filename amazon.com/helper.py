from lxml import html

def get_ASIN(parser,XPATH):
	XPATH_ASIN = XPATH + '/@data-asin'
	try:
		raw_asin = parser.xpath(XPATH_ASIN)
		return raw_asin[0]
	except IndexError as e:
		# print("raw_asin:",raw_asin,"error:",e)
		return None

def get_name(parser,XPATH):
	# fetch name from data

	XPATH_NAME = XPATH + '/div[last()]//h2//text()'					
	try:
		raw_name = parser.xpath(XPATH_NAME)
		return raw_name[0]
	except :
		try:
									
			raw_name = parser.xpath(XPATH + '/div[last()]//a[@class="a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"]/@title')
			return raw_name[0]
		except:
			return None

def get_price(parser,XPATH):
	# Fetch the price range(min-max)

	XPATH_PRICE = XPATH + '/div[last()]//span[@class="sx-price-whole"]//text()'
	XPATH_CENTS = XPATH + '/div[last()]//sup[@class="sx-price-fractional"]//text()'
	try:
		raw_price = parser.xpath(XPATH_PRICE)
		raw_cents = parser.xpath(XPATH_CENTS)
		PRICE = int(raw_price[0].replace(',','')) + 0.01 * int(raw_cents[0])
		return PRICE
	except Exception as e:
		# print("raw_price:",raw_price,e)
		return None			

def get_star(parser,XPATH):
	# Fetch the rating

	XPATH_STARS = XPATH + '/div[last()]//a[@class="a-popover-trigger a-declarative"]//text()' 
	try:
		raw_stars = parser.xpath(XPATH_STARS)
		y = ''.join(raw_stars[0]).split()					
		for num in y:
				num = num.replace(',','')
				try:
					return float(num)
					break
				except ValueError:
					pass
	except IndexError:
		return 0

def get_reviews(parser,XPATH,price):
	# Fetch the number of reviews 

	XPATH_REVIEWS = XPATH + '/div[last()]//a[@class="a-size-small a-link-normal a-text-normal"]//text()'
	try:
		raw_reviews = parser.xpath(XPATH_REVIEWS)
		if len(raw_reviews) == 1:
			reviews = raw_reviews[0]
			reviews = float(reviews.replace(',',''))
			return price,reviews
		elif len(raw_reviews) > 1:
			price_index = raw_reviews.index(u'\xa0\xa0') + 1
			price = [float(raw_reviews[price_index].replace(',',''))]
			reviews = [ float(raw_reviews[review_index].replace(',','')) for review_index in range(price_index+1,len(raw_reviews))]
			return price,reviews
		else:
			return price,0
	except IndexError:
		return price,0
	except ValueError as v:
		return price,0
		print(raw_reviews,v)		

