from scrapy.spiders import SitemapSpider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import scrapy
import os,re
import requests
import des

class MySpider(SitemapSpider):
	name='Arania'
	contador=0
	
	def __init__(self, url,ruta, *a, **kw):
        	super(MySpider, self).__init__(*a,**kw)
		self.contador=0
		self.ruta_destino=ruta

		if 'list' in str(type(url)):
			self.sitemap_urls=tuple(url)
		if 'str' in str(type(url)):
			self.sitemap_urls=(url,)
		if 'tuple' in str(type(url)):
			self.sitemap_urls=url
		
		self.custom_settings={'LOG_ENABLED': False}
		print type(self.sitemap_urls)
		print self.sitemap_urls
	

	def parse(self, response):
		print "#####################################################"
		print response.url		
		print "#####################################################"

		ext=response.url.split('.')[-1]

		if ext=='pdf' or ext=='docx' or ext=='doc' or ext=='xlsx' or ext=='xls' or ext=='ppt' or ext=='pptx':
			des.fun_descargar(response.url,self.ruta_destino)

		return
			

def download_from_sitemap(enlaces,ruta_d):
	runner= CrawlerRunner({'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
	d=runner.crawl(MySpider,url=enlaces,ruta=ruta_d,a=(),kw={})
	d.addBoth(lambda _: reactor.stop())
	reactor.run()













