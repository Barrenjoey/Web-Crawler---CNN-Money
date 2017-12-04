import bs4 as bs
import urllib.request
import re
import datetime
import os
"""
#__WebCrawler__#
This is a simple web crawler designed for extracting urls from the CNN Money website.
It will save desired urls, which in this case is news articles, to _Wanted_URLS.txt, 
and it will also create a crawled file to prevent duplicated crawls in the future.
"""
#Change this to where you want the urls saved to.
saveLocation = "D:/Desktop/"
#Date
date = datetime.date.today()
#Date of today and yesterday
today = datetime.datetime.now()
today = today.day
#Month - text
month = datetime.datetime.now()
month_int = month.month
month = month.strftime("%B")

#Starting Url and declared variables etc..
start_url = "http://money.cnn.com/"
spider_list = []
crawled_list = []
scrape_list = []
scrapeD_list = []
crawler_url = ""
http_scan = re.compile('http')
video_scan = re.compile('/video/')
money_scan = re.compile('http://money.cnn.com/')
index_scan = re.compile('index.html?')
loop_counter = 0
mainLoop = True

#Test URL, exception if error
try:
	sauce = urllib.request.urlopen(start_url).read()
except Exception as e:			
	print(str(e))
	
#Converting website html to Beautiful Soup	
sauce = urllib.request.urlopen(start_url).read()
soup =	bs.BeautifulSoup(sauce, 'lxml')

#Importing already crawled urls and adding to crawled list.
try:
	with open("D:/Desktop/_CRAWLED_URLS.txt") as f:
		crawled_list = f.readlines()
	crawled_list = [x.strip() for x in crawled_list] 
	crawled_list = list(set(crawled_list))	
except Exception as e:
	print('IMPORTING CRAWLED URLS ERROR! ' + str(e))
#Importing already scraped urls	
try:
	with open("D:/Desktop/_Wanted_URLS.txt") as f:
		scrapeD_list = f.readlines()
	scrapeD_list = [x.strip() for x in scrapeD_list] 
	scrapeD_list = list(set(scrapeD_list))	
except Exception as e:
	print('IMPORTING SCRAPE URLS ERROR! ' + str(e))	

#Finding all the url links on the page, removing http links, adding starting_url and adding to list.
def url_finder():
	for link in soup.find_all('a'):
		new_url = link.get('href')
#Searching for money website at start of url and adding to url list		
		tt = re.findall(money_scan, str(new_url))
		kk = re.findall(http_scan, str(new_url))
		if len(tt) > 0:
			if new_url not in spider_list:
				spider_list.append(new_url)
#Searching for http (other sites) and only adding urls that dont have http.				
		elif len(kk) == 0:	
			new_url = start_url + str(new_url)
			if new_url not in spider_list:
				spider_list.append(new_url)
		else:
			pass
#Taking wanted urls from spider_list to scrape_list.
def wanted_urls():
	for url in spider_list:
		zz = re.findall(index_scan, str(url))
		if url.endswith('index.html'):
			jj = re.findall(video_scan, str(url))
			if len(jj) <= 0:
				if url not in scrape_list and url not in scrapeD_list:
					scrape_list.append(url)
					print(url)	
		elif len(zz) > 0:
			if url not in scrape_list and url not in scrapeD_list:
				scrape_list.append(url)
				print(url)
url_finder()
wanted_urls()

#Looping through url list, looking for more urls and adding wanted urls to scrape list. Delete index range cap to run until it has crawled all available.
while mainLoop:
	for url in spider_list[0:5]:
		if url not in crawled_list:
			print("Trying URL: ", url)
			loop_counter += 1
			print(loop_counter)
			crawler_url = url
			try:
				sauce = urllib.request.urlopen(crawler_url).read()
			except Exception as e:			
				print(str(e))		
#Converting website html to Beautiful Soup	
			try:
				sauce = urllib.request.urlopen(crawler_url).read()
				soup =	bs.BeautifulSoup(sauce, 'lxml')
			except Exception as e:
				print("FAILED!!SOUP: ",url)
				print(str(e))
			try:
				url_finder()
			except Exception as e:
				print("FAILED!!1: "+ url)
				print(str(e))
			try:	
				wanted_urls()
			except Exception as e:
				print("FAILED!!2: "+ url)
				print(str(e))
#Adding crawled url to crawled list and checking whether the loop needs to end.		
			crawled_list.append(url)
			if len(spider_list) == len(crawled_list):
				mainLoop = False
			print("Spider: ",len(spider_list))
			print("Scrape: ",len(scrape_list))
			print("Crawled: ", len(crawled_list))
	break
# print(spider_list)
print("Spider: ",len(spider_list))
#print(scrape_list)
print("Scrape: ",len(scrape_list))

#Creating crawled text file to stop later crawls of same thing.
saveFile = open(saveLocation + '_CRAWLED_URLS.txt', 'w')
saveFile.close()
for item in crawled_list:
	saveFile = open(saveLocation + '_CRAWLED_URLS.txt', 'a')		
	saveFile.write(str(item) + "\n")
	saveFile.close()

#Saving scrape url text file for scraping.
for item in scrape_list:
	saveFile = open(saveLocation + '_Wanted_URLS.txt', 'a')		
	saveFile.write(str(item) + "\n")
	saveFile.close()
	