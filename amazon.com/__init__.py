import threading,json
from get_input import *
from request_maker import request_page

ITEMS = [] 				# Stores the data 

THREADS = 10			# No. of threads      

# These functions are defined in get_input.py
URL = category()		#Url to hit		
TOTAL_PAGES = amount_data()		# Total number of pages to extract

THREAD_PAGE = int(TOTAL_PAGES/THREADS)  	# No. of pages per thread


file_name = get_filename()		#File to store the data as json


def worker(index):
	# Loops through all the pages
	for i in range(index*THREAD_PAGE ,(index+1)*THREAD_PAGE):
		block = request_page( URL + '&page=' +str(i))
		# print(block)
		ITEMS.append(block)


## Code execution begins from here ##
thread_working = []
for i in range(min(THREADS,TOTAL_PAGES)) :
	t = threading.Thread(target=worker,args=(i,))
	thread_working.append(t)
	t.start() #start the threads

for x in thread_working:
	x.join()	

#  After Completion store it in a file
with open(file_name, "w+") as jsonFile:
	json.dump(ITEMS,jsonFile,indent=4)	