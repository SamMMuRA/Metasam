import requests, re
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Obtener los enlaces sitemap xml de un dominio.

def get_sitemap(domain):
	'''
	Conseguir el sitemap de un dominio.Simplemente le proporcionas un dominio. Devuelve una lista con enlaces apuntando a los sitemaps. 
	'''
	sitemaps=[]
	error=0
	user_agent='Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'

	warnings.simplefilter('ignore',InsecureRequestWarning)
	
	ssn = requests.Session()
	ssn.headers={'User-Agent':user_agent}
	link='http://www.'+ domain + '/robots.txt'

	try:
		res=ssn.head(link,allow_redirects=True,timeout=15)
	except:
		error=1
		pass	

	if error == 0:
		if res.status_code == 200:
			res=ssn.get(link, allow_redirects=True,timeout=15)
			xmls=re.findall(r'Sitemap:.*https?://.*\.xml',res.content)

			for i in xmls:
				sitemaps.append(i.split('Sitemap:')[1].replace(' ',''))

	error=0
	ssn = requests.Session()
	ssn.headers={'User-Agent':user_agent}
	link='https://www.'+ domain + '/robots.txt'

	try:
		res=ssn.head(link,allow_redirects=True,timeout=15)
	except:
		error=1
		pass

	if error == 0:	
		if res.status_code == 200:
			res=ssn.get(link, allow_redirects=True,timeout=15)
			xmls=re.findall(r'Sitemap:.*https?://.*\.xml',res.content)

			for i in xmls:
				sitemaps.append(i.split('Sitemap:')[1].replace(' ',''))

	error=0

	#Llegados a este punto en sitemaps solo se ha buscado en robots.txt enlaces sitemap.xml
	#Continuamos buscando los sitemap directamente.
	
	ssn = requests.Session()
	ssn.headers={'User-Agent':user_agent}
	link='http://www.'+ domain + '/sitemap.xml'

	try:
		res=ssn.head(link,allow_redirects=True,timeout=15)
	except:
		error=1
		pass	

	if error == 0:	
		if res.status_code == 200:
			res=ssn.get(link, allow_redirects=True,timeout=15)
			if '<url>' in res.content:
				print '<url>'
				sitemaps.append(link)
		
			if '</sitemapindex>' in res.content:
				print '<sitemapindex>'
				sitemaps.append(link)

	error=0

	ssn = requests.Session()
	ssn.headers={'User-Agent':user_agent}
	link='https://www.'+ domain + '/sitemap.xml'
	print link

	try:
		res=ssn.head(link,allow_redirects=True,timeout=15,verify=False)

	except:
		error=1
		pass	

	if error == 0:	
		if res.status_code == 200:
			res=ssn.get(link, allow_redirects=True,timeout=15,verify=False)
			if '<url>' in res.content:
				sitemaps.append(link)
			
			if '</sitemapindex>' in res.content:
				print '<sitemapindex>'
				sitemaps.append(link)

	error=0

	#print len(sitemaps)

	if len(sitemaps)>0:
		return list(set(sitemaps))
	else:
		print "No se han encontrado sitemaps"
		return sitemaps



if __name__=='__main__':
	dominio=raw_input('>Introduce el dominio:').rstrip('\r\n')
	urls=get_sitemap(dominio)
	print urls



