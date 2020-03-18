import pycurl,os

def fun_descargar(lnk,ruta_o):
	nam=lnk.split('/')[-1]
	c = pycurl.Curl()
	c.setopt(c.URL, lnk)
	c.setopt(pycurl.SSL_VERIFYPEER,False)
	c.setopt(pycurl.SSL_VERIFYHOST,False)

	wkd=os.getcwd()
	os.chdir(ruta_o)	

	with open(nam, 'w') as f:
    		c.setopt(c.WRITEFUNCTION, f.write)
    		c.perform()
		f.close()
	
	os.chdir(wkd)


if __name__=="__main__":

	#ruta=raw_input('> Introduce una ruta absoluta en el sistema para guardar el documento:\r\n')
	enl=raw_input('> Introduce un enlace de descarga:\r\n')
	
	ruta=raw_input('> Introduce una ruta para el fichero:\r\n').rstrip('\r\n')
	fun_descargar(enl,ruta)
	#os.rename("nam",ruta + '/' + nam)

