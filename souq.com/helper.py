from lxml import html

def get_name(parser,XPATH):
	# fetch name from data

	XPATH_NAME = XPATH + '/@data-name' 					
	try:
		raw_name = parser.xpath(XPATH_NAME)
		return raw_name[0]
	except :
		return None

def get_brand_name(parser,XPATH):
	# fetch name from data

	XPATH_BRAND_NAME = XPATH + '/@data-brand-name' 					
	try:
		raw_brand_name = parser.xpath(XPATH_BRAND_NAME)
		return raw_brand_name[0]
	except :
		return None		


def get_category_name(parser,XPATH):
	# fetch name from data

	XPATH_CAT_NAME = XPATH + '/@data-category-name' 					
	try:
		raw_cat_name = parser.xpath(XPATH_CAT_NAME)
		return raw_cat_name[0]
	except :
		return None

def get_price(parser,XPATH):
	# Fetch the price range(min-max)
	XPRICE = XPATH + '//span[@class="itemPrice"]//text()'	

	try:
		raw_price = parser.xpath(XPRICE)
		return raw_price[0]
	except Exception as e:
		# print("raw_price:",raw_price,e)
		return None			


def get_real_price(parser,XPATH,price):
	# Fetch the price range(min-max)
	X_REAL_PRICE = XPATH + '//span[contains(@class,"itemOldPrice")]//text()'	
	try:
		raw_real_price = parser.xpath(X_REAL_PRICE)
		real_price = raw_real_price[0].replace('AED','')
		return real_price,cal_discount(real_price,price)
	except IndexError as i:
		return price,cal_discount(price,price)	
	except Exception as e:
		print("real_price:",e)
		return None,None		

def cal_discount(real_price,actual_price):
	RP = float(real_price.replace(',',''))
	AP = float(actual_price.replace(',',''))
	return (100*(RP-AP))/RP

def get_star(parser,XPATH):
	# Fetch the rating

	XPATH_STARS = XPATH + '//span[@class="rating-stars"]/i/i/@style'
	try:
		raw_star = parser.xpath(XPATH_STARS)
		return raw_star[0].replace('width:','').replace('%','')
	except IndexError as i :
		return '0'
	
	except Exception as e:
		return None

def get_shipping(parser,XPATH):
	X_Shiping = XPATH + '//strong[@class="green-text"]//text()'
	try:
		raw_ship = parser.xpath(X_Shiping)
		if raw_ship[0]:
			return True
	except Exception as e:
		return False