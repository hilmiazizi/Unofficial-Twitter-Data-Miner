# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import os
from langdetect import detect
import argparse
import datetime
from urlextract import URLExtract
os.system('clear')
counter = 0

def DataWriter(datas):
	global today
	global keyword
	file_name = keyword+' - '+today.replace('/','-')+'.csv'
	result = open(file_name,'a+')
	result.write(datas+"\n")
	result.close()

def TimeConfig(n_day):
	period_datas = []
	today = datetime.datetime.now()
	for i in range(0,n_day):
		period = today - datetime.timedelta(days=i)
		period_datas.append(period.strftime('%d/%m/%Y').replace('/0','/'))
	return today.strftime('%d/%m/%Y'),period_datas


def Extractor(response):
	global max_tweet
	global period_datas
	global counter
	global lang
	soup = BeautifulSoup(response, 'html.parser')
	content = soup.find_all('div', class_='timeline-item')
	for datas in content:
		if 'Load newest' in str(datas):
			continue
		#########################################
		# Extracting Tweet's Date 
		#########################################
		for line in str(datas).splitlines():
			if 'title="' in line and 'status' in line and 'Load newest' not in line:
				tweet_date = re.search('title="(.*), ', line).group(1)
				if tweet_date in period_datas:
					valid_date = True
					break
				else:
					valid_date = False
					break

		if not valid_date:
			continue
		#########################################
		# Making different soup for each tweet
		#########################################
		scraper = BeautifulSoup(str(datas), 'html.parser')


		#########################################
		# Tweet's Stats Extract Part
		#########################################
		stats = scraper.find_all('div', class_='tweet-stats')
		for tweet_stats in stats:
			for temp in str(tweet_stats).splitlines():
				if 'icon-comment' in temp:
					tweet_comment = re.search('><span class="icon-comment" title=""></span> (.*)</div></span>', temp).group(1)
					tweet_comment = int(tweet_comment.replace(',',''))

				if 'icon-retweet' in temp:
					tweet_retweet = re.search('><span class="icon-retweet" title=""></span> (.*)</div></span>', temp).group(1)
					tweet_retweet = int(tweet_retweet.replace(',',''))

				if 'icon-quote' in temp:
					tweet_quote = re.search('><span class="icon-quote" title=""></span> (.*)</div></span>', temp).group(1)
					tweet_quote = int(tweet_quote.replace(',',''))

				if 'icon-heart' in temp:
					tweet_like = re.search('><span class="icon-heart" title=""></span> (.*)</div></span>', temp).group(1)
					tweet_like = int(tweet_like.replace(',',''))

		tweet_username = scraper.find('a', class_='username').get_text()
		tweet_fullname = scraper.find('a', class_='fullname').get_text()


		tweet_content = scraper.find('div', class_='tweet-content media-body').get_text().replace(',','.').replace('\n','. ')
		try:
			tweet_lang = detect(tweet_content)
			if tweet_lang != lang:
				continue
			else:
				counter+=1
		except:
			continue
		extractor = URLExtract()
		urls = extractor.find_urls(tweet_content)
		if urls:
			has_links = True
		else:
			has_links = False

		if 'icon-ok verified-icon' in str(datas):
			tweet_is_verified = True
		else:
			tweet_is_verified = False
		if 'Replying to' in str(datas):
			tweet_is_reply = True
		else:
			tweet_is_reply = False

		result = tweet_date+','+tweet_username+','+tweet_fullname+','+str(tweet_is_verified)+','+str(tweet_is_reply)+','+str(has_links)+','+str(tweet_content)+','+str(tweet_comment)+','+str(tweet_retweet)+','+str(tweet_quote)+','+str(tweet_like)
		DataWriter(result)
		if max_tweet == counter:
			return False
			
	#########################################
	# Extracting Cursor for next page
	#########################################
	cursor = re.search('cursor=(.*)">Load more', str(response))
	if max_tweet>counter:
		return True

def ScrapeFirst(keyword):
	headers = {
	    'Host': 'nitter.pussthecat.org',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	    'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
	    'Accept-Encoding': 'gzip, deflate',
	    'Upgrade-Insecure-Requests': '1',
	    'Sec-Fetch-Dest': 'document',
	    'Sec-Fetch-Mode': 'navigate',
	    'Sec-Fetch-Site': 'none',
	    'Sec-Fetch-User': '?1',
	    'Te': 'trailers',
	    'Connection': 'close',
	}

	params = (
	    ('f', 'tweets'),
	    ('q', keyword),
	)

	response = requests.get('https://nitter.pussthecat.org/search', headers=headers, params=params)
	status = Extractor(response.text)
	if not status:
		return
	try:
		cursor = re.search('cursor=scroll%3A(.*)">Loa', response.text).group(1)
		NextScrape(cursor,keyword)
	except Exception as e:
		print(str(e))
		return

def NextScrape(cursor,keyword):
	headers = {
	    'Host': 'nitter.pussthecat.org',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0',
	    'Accept': '*/*',
	    'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
	    'Accept-Encoding': 'gzip, deflate',
	    'Sec-Fetch-Dest': 'empty',
	    'Sec-Fetch-Mode': 'cors',
	    'Sec-Fetch-Site': 'same-origin',
	    'Te': 'trailers',
	}

	params = (
	    ('f', 'tweets'),
	    ('q', keyword),
	    ('cursor', 'scroll:'+cursor),
	    ('scroll', 'true'),
	)

	response = requests.get('https://nitter.pussthecat.org/search', headers=headers, params=params)
	status = Extractor(response.text)
	if not status:
		return
	try:
		cursor = re.search('cursor=scroll%3A(.*)">Loa', str(response.text)).group(1)
		NextScrape(cursor,keyword)
	except Exception as e:
		print(str(e))
		return


#########################################
# Argument Parser
#########################################
parser = argparse.ArgumentParser()
parser.add_argument('--period', type=int, required=True, help="Tweets period in number, example: 7, will scape tweets from today to 7 days ago")
parser.add_argument('--keyword', type=str, required=True, help="Keyword, please use quote")
parser.add_argument('--max', type=int, required=True, help="Maximum tweets scrapped")
parser.add_argument('--lang', type=str, required=True, help="Language in ISO 639-1 codes, check on https://pypi.org/project/langdetect/")
args = parser.parse_args()

today, period_datas = TimeConfig(args.period)
keyword = args.keyword
lang = args.lang
max_tweet = args.max
file_name = keyword+' - '+today.replace('/','-')+'.csv'
result = open(file_name,'a+')
result.write('Tweet Date,Username,Full Name,Verfied,Is Reply,Has Links,Content,Comments,Retweet,Quote,Likes\n')
result.close()

print(' '*10+'-*- Twitter Data Miner -*-')
print('Keyword\t\t:', args.keyword)
print('Maximum Tweet\t:', args.max)
print('Tweets Period\t:',args.period,'day')
print('Output File\t:', file_name)

ScrapeFirst(keyword)
print(' '*16+'-*- Done -*-\n\n')

