from pyfiglet import Figlet
import des,g_sitemap,meta,spider_sitemap

#from metasam import des,g_sitemap,meta,spider_sitemap
import time,sys


def main():

	f=Figlet(font='slant')

	print '\033[94m' + f.renderText('MetaSam')

	print '\r\n______________________________________Samir Kamal Moreno_________'


	domain=raw_input("[*]Introduce dominio:")

	sits=g_sitemap.get_sitemap(domain)

	print '>> Estos son los sitemaps:'

	print sits

	rutad=raw_input("[*]Introduce ruta destino:")

	try:
		spider_sitemap.download_from_sitemap(sits,rutad)
	except:
		print "[*]You don`t want fair play ........ :{\r\n"

		print '\033[94m' + f.renderText('Bye :{')
	
	i=0


	while i < 5:
		print '\033[94m' + 'Reporting >',
		time.sleep(.300) 
		print '\r',
		print '\033[92m' + 'Reporting >>',
		time.sleep(.300)
		print '\r',
		print '\033[93m' + 'Reporting >>>',
		time.sleep(.300)
		print '\r',
		i=i+1

	d=meta.generar_meta_csv(rutad,'metadata.csv')

	meta.generate_report(d)

	print '\033[92m' + f.renderText('Hurra!!! Done')

	print '\033[93m' + '_____________________________________Report Done [metadata.csv/Report.pdf]'



if __name__=="__main__":
	main()
	



