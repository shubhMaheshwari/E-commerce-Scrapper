import json


with open('amazon_urls.json','r') as jsonFile:
	url_dict = json.loads(jsonFile.read())


def category():
	
	while True:
		try:
			for index,elem in enumerate(url_dict):
				print(str(index) + ") " + elem)

			ind = input("\nSelect Category(number):")

			return "https://www.amazon.com" + list(url_dict.values())[int(ind)]
		except IndexError:
			input("\n\nEnter a number present the list. (Press Enter to continue)")

		except ValueError:
			input("\n\nEnter a number in the list. (Press Enter to continue)")	
			

def amount_data():
	while True:
		try:
			num_pages = input("Enter the number of pages to extract(default 1000):")
			if num_pages == '':
				return 1000
			return int(num_pages)
		except Exception as e:
			print("Input a number",e)			


def get_filename():
	while True:
		try:
			fileName = input("Enter the file name(default data.json):")
			print("Filename",fileName)
			if fileName == '':
				return "data.json"
			return fileName
		except NameError as n:
			return "data.json"	
		except Exception as e:
			print("Input a filename",e)				