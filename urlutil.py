'''
#v.20191216.0
# -*- coding: utf-8 -*-

import re, glob
from logging import getLogger, handlers, Formatter, StreamHandler, DEBUG
import argparse
import urllib.request
import urllib.parse
import http.cookiejar
import requests

class Urlutil:
	def __init__(self, url_ref = ""):
		self.ua = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100',
					'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36']
		self.setOpener(url_ref)
	
	def setOpener(self, url_ref):
		cookiejar = http.cookiejar.CookieJar()
		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
		opener.addheaders = [('User-Agent', self.ua[0],)]
		opener.addheaders = [('Referer',url_ref)]
		urllib.request.install_opener(opener)
	
	def getSoup(self, url_soup, tag, attr = None, query = None):
		try:
			from bs4 import BeautifulSoup
		except Exception as e:
			logger.debug('BeautifulSoup import Err: ' + str(e))
			return None
		try:
			response = urllib.request.urlopen(url_soup)
		except Exception as e:
			logger.debug('getSoup: ' + str(e) + ': ' + response.text)
			return None
		html = response.read().decode('utf-8', errors='ignore')
		soup = BeautifulSoup(html, 'html.parser')
		try:
			if attr is "href":
				pages = soup.find_all(tag, href=re.compile(query))
			elif attr is "class":
				pages = soup.find_all(tag, class_=re.compile(query))
			elif attr is "title":
				pages = soup.find_all(tag, title=re.compile(query))
			elif attr is "id":
				pages = soup.find_all(tag, id=re.compile(query))
			else:
				pages = soup.find_all(tag)
		except Exception as e:
			logger.debug('getSoup: ' + str(e))
			return None
		return pages
	
	def checkLink(self, url_ck):
		parse = urllib.parse.urlparse(url_ck)
		loc = parse.scheme + "://" + parse.netloc + "/"
		locs = []
		try:
			links = self.getSoup(url_ck, "a")
			for i in links:
				link = i.get("href")
				if re.compile("^\/").search(link):
					url = loc + link.replace('/','')
				elif not re.compile("^http").search(link):
					url = loc + link
				else:
					continue
				locs.append(url)
			return locs
		except Exception as e:
			logger.debug('checkLink: ' + str(e))
			return None
	
	def postPass(self, url_post, params):
		#link = self.getSoup(url_post, "input", "type", "password")
		#for i in link:
		#	print(i)
		s = requests.Session()
		#params={'username':'user','password':'pass','mode':'login'})
		r = s.post(url_post, params=params)
		res = requests.get()
		with open(pwd + file_name, 'w') as f:
		       f.write(r.text)
		return r
	

def download(url, path, file_name):
	file_name = re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '-', file_name)
	if file_name[0] == "/":
		file_name = file_name[1:]
	if path[-1:] != "/":
		path = path + "/"
	if glob.glob(path + file_name + "*"):
		print(file_name + " exitsts.")
	try:
		urllib.request.urlretrieve(dl_url, path + file_name)
	except Exception as e:
		logger.debug('download: ' + str(e))
	
def help():
	print("""class
	Urlutil()
method
	referer(url_ref)	Set referer.
	getSoup(url, tag, attr = None, que = None)	Return pages.
	checkLink(url)		Return local-links.
	post(url, post)		Return response.
function
	download(url, path, file_name)""")

def _logger():
	logger = getLogger(__name__)
	logger.setLevel(DEBUG)
	formatter = Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")
	handler_console = StreamHandler()
	handler_console.setLevel(DEBUG)
	handler_console.setFormatter(formatter)
	logger.addHandler(handler_console)
	handler_file = handlers.RotatingFileHandler(filename='./Urlutil.log',maxBytes=1048576,backupCount=3)
	handler_file.setFormatter(formatter)
	logger.addHandler(handler_file)
	logger.propagate = False
	return logger

def _parser():
	parser = argparse.ArgumentParser(
		usage="""twiutil.py getUserMedia [screen_name]
	twiutil.py searchWord2Json [screen_name] --keyword '<search_word> --output <output_file>'""",
		add_help=True,
		formatter_class=argparse.RawTextHelpFormatter
	)
	parser.add_argument("mode", help="", type=str, metavar="[mode]")
	parser.add_argument("screen_name", help="", type=str, metavar="[screen_name]")
	parser.add_argument("--user_id", help="", type=int, metavar="<user_id>")
	parser.add_argument("--keyword", help="", type=str, nargs='*', metavar="'<keyword>'")
	parser.add_argument("--output", help="", type=str, metavar="'<output_file>'")
	return parser.parse_args()

def _main():
	import sys,datetime
	datetime_format = datetime.date.today()
	datetime_format = datetime_format - datetime.timedelta(days=1)
	datetime_today = datetime_format.strftime("%Y%m%d")
	check_link(url)

if __name__ == '__main__':
	logger = _logger()
	_main()
else:
	logger = _logger()
	help()
'''