import bs4 as bs
import urllib.request
import re
import os
import datetime
import sqlite3
'''WebScraper - CNN Money.
This WebScraper is designed to scrape the content from the CNN-Money URLS which were gathered
from the WebCrawler. It gets the URLS from a text-file and then saves the content to a database.
'''
#Change this to where you want the urls saved to.
saveLocation = "D:/Desktop/"
#Change to True if you want scraped text documents as well as database.
createTextDoc = True
#Date
date = datetime.date.today()
#Date of today and yesterday
today = datetime.datetime.now()
today = today.day
#Month - text
month = datetime.datetime.now()
month = month.strftime("%B")

######################################################
#Connecting to database and creating cursor
conn = sqlite3.connect('Sentiment_Analysis.db')
c = conn.cursor()
#Create table function
def create_table():
	c.execute("CREATE TABLE IF NOT EXISTS Crawled_Data(url TEXT PRIMARY KEY, article_date TEXT, source TEXT, location TEXT, title TEXT, content TEXT, date_scraped TEXT, date_analysed TEXT)")
	#7 categories
def data_entry():
	c.execute("INSERT INTO Crawled_Data (url, article_date, source, location, title, content, date_scraped) VALUES (?, ?, ?, ?, ?, ?, ?)", (url, article_date, 'CNN Money', 'location', title, content, date))
	conn.commit()
def select_data():
	c.execute("SELECT url FROM Crawled_Data")
	data = c.fetchall()
	#data = data[0]
	for cell in data:
		cell = cell[0]
		if cell == url:
			del_and_update()
def del_and_update():
	c.execute("SELECT * FROM Crawled_Data")
	dat = c.fetchall()
	c.execute("DELETE FROM Crawled_Data WHERE url=?", (url,))
	conn.commit()
	data_entry()

create_table()	
#########################################################

body_text = ""
para_string = ""
#Counter
counter = 1
#Extracting URLS from URL text file into a list
with open(saveLocation + "_Wanted_URLS.txt") as f:
	url_list = f.readlines()
# Remove whitespace characters like `\n` at the end of each line
url_list = [x.strip() for x in url_list]
#Accessing each url from the list to scrape
for url in url_list[0: ]:
	print (url)
	try:
		#Selecting URL ############################################
		sauce = urllib.request.urlopen(url).read()
		soup =  bs.BeautifulSoup(sauce, 'lxml')		
		#Making html pretty
		# x = soup.prettify()		
		# print(x)
		
		#Find title ################################################
		title = soup.h1.string
		
		#Find h2 topic sentence #########################################
		for div in soup.find_all('h2'):		
			try:
				h2_title = str(div.contents[0])	
			except Exception as e:
				print("H2 ERROR!!" + str(e))	
		#Finding date of article ####################################	
		article_date = soup.find_all("meta", {"name": "date"})
		#Narrowing search with RegEx
		article_date = re.findall(r'(\d+-\d+-\d+)', str(article_date))
		article_date = article_date[0]
		article_date = re.sub(r'-', '/', article_date)
		if createTextDoc:
			#Saving date and creating text file
			saveFile = open(saveLocation + "/" + str(counter) + '#Article_money.txt', 'w')	
			saveFile.write(str(article_date))
			saveFile.close()
			#Save title		
			saveFile = open(saveLocation + "/" + str(counter) + '#Article_money.txt', 'a')	
			saveFile.write(str("\n" + "#" + title + "#"))
			saveFile.close()

		for content in soup.find_all('div',{"id": "storytext"}):	#Find content
			try:
				for item in soup.find_all('p'):
					paragraph = re.findall(r'>(.*?)<', str(item))
					for i in paragraph:
						para_string = para_string + i
					body_text = body_text + para_string	
					para_string = ""
			except Exception as e:			
				print("ERROR SCRAPING BODY TEXT!!" + str(e))
				
		content = "#" + title + "#. " + h2_title + body_text
		content = re.sub(r'<(.*?)>', '', content) ########### Maybe the golden phrase?
		if createTextDoc:
			saveFile = open(saveLocation + "/" + str(counter) + '#Article_money.txt', 'a')	
			saveFile.write(str("\n" + content))
			saveFile.close()
#Data entry and select, delete and update if url already present.
		try:
			data_entry()
		except Exception as e:
			print("URL PRESENT: " + str(e))
			try:
				select_data()
			except Exception as e:
				print("DATA ENTRY FAILED!!: " + str(e))
		body_text = ""
		h2_title = ""
		content = ""
		title = ""		
		print (counter)
		counter += 1
	except Exception as e:			
		print("MAIN SCRAPE ERROR!!" + str(e))
c.close()
conn.close()
	
# if __name__ == "__main__":
	# main()