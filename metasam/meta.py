import zipfile, lxml.etree, re, os
from pyPdf import PdfFileReader
import unidecode, magic
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

def analizar_file(fichero):

	ext=fichero.split('.')[-1]
	extension=magic.from_file(fichero)

	if 'PDF' in extension:
		#Procederemos a analizar metadatos de un fichero pdf

		metadata_pdf={}
		tipo_metadatos=['Title','CreationDate','Author','Producer','Creator','ModDate','Company','Comments','Keywords','SourceModified','Subject']
		
		try:
			pdf_toread = PdfFileReader(open(fichero, "rb"))
		except:
			return metadata_pdf

		pdf_info = pdf_toread.getDocumentInfo()

		for i in tipo_metadatos:
			metadata_pdf.update({i:'#'})
	
		for k,v in pdf_info.iteritems():
			metadata_pdf.update({unidecode.unidecode(unicode(k.split('/')[1])):unidecode.unidecode(unicode(v))})
			#metadata_pdf.append(v)
	
		metadata_pdf.update({'Fichero':fichero})
		metadata_pdf.update({'Tipo':'PDF'})

		return metadata_pdf

	if ext=='doc' or ext=='ppt' or ext=='xls':
		#Es un formato antiguo de fichero Office, no son .zip, hay que analizarlos de otra manera.
		info=magic.from_file(fichero)
		
		#print info

		title=re.findall(r'Title:.*',info)
		if len(title)>0:
			title=title[0].split(':')[1].split(',')[0]
		else:
			title='#'
		

		author=re.findall(r'Author:.*',info)
		if len(author)>0:
			author=author[0].split(':')[1].split(',')[0]
		else:
			author='#'

		lastsavedby=re.findall(r'Last Saved By:.*',info)
		if len(lastsavedby)>0:
			lastsavedby=lastsavedby[0].split(':')[1].split(',')[0]
		else:
			lastsavedby='#'

		revision=re.findall(r'Revision Number:.*',info)
		if len(revision)>0:
			revision=revision[0].split(':')[1].split(',')[0]
		else:
			revision='#'

		aplication=re.findall(r'Creating Application:.*',info)
		if len(aplication)>0:
			aplication=aplication[0].split(':')[1].split(',')[0]
		else:
			aplication='#'

		created=re.findall(r'Create Time/Date:.*',info)
		if len(created)>0:
			created=created[0].split(':')[1].split(',')[0]
		else:
			created='#'

		lastsaved=re.findall(r'Saved Time/Date:.*',info)
		if len(lastsaved)>0:
			lastsaved=lastsaved[0].split(':')[1].split(',')[0]
		else:
			lastsaved='#'

		pages=re.findall(r'Pages:.*',info)
		if len(pages)>0:
			pages=pages[0].split(':')[1].split(',')[0]
		else:
			pages='#'

		words=re.findall(r'Words:.*',info)
		if len(words)>0:
			words=words[0].split(':')[1].split(',')[0]
		else:
			words='#'

		chars=re.findall(r'Characters:.*',info)
		if len(chars)>0:
			chars=chars[0].split(':')[1].split(',')[0]
		else:
			chars='#'

		lastprinted=re.findall(r'Last Printed:.*',info)
		if len(lastprinted)>0:
			lastprinted=lastprinted[0].split(':')[1].split(',')[0]
		else:
			lastprinted='#'


		res={
			'Fichero':fichero,
			'Tipo':ext,
			'creator':author,
			'lastModifiedBy':lastsavedby,
			'created':created,
			'modified':lastsaved,
			'title':title,
			'revision':revision,
			'lastPrinted':lastprinted,
			'keywords':'#',
			'Application':aplication,
			'Paginas':pages,
			'Palabras':words,
			'Caracteres':chars,
			'Lineas':'#',
			'Parrafos':'#',
			'Slides':'#',
			'PresentationFormat':'#'
		}

		return res

	if 'Word' in extension or 'Excel' in extension or 'PowerPoint' in extension:
		try:
			zf=zipfile.ZipFile(fichero)
		except:
			return {}
		
		#Analizamos el fichero core.xml y sacamos metadatos de ahi.
		core_xml=zf.read('docProps/core.xml')
		
		xmlns_cp=re.findall(r'xmlns:cp="https?:.*"',core_xml)
		xmlns_cp=xmlns_cp[0].split('"')[1]
		#print xmlns_cp
	
		xmlns_dc=re.findall(r'xmlns:dc="https?:.*"',core_xml)
		xmlns_dc=xmlns_dc[0].split('"')[1]
		#print xmlns_dc

		xmlns_dcterms=re.findall(r'xmlns:dcterms="https?:.*"',core_xml)
		xmlns_dcterms=xmlns_dcterms[0].split('"')[1]
		#print xmlns_dcterms


		doc=lxml.etree.fromstring(core_xml)

		# Ya hemos creado las variables para crear el diccionario namespace
		ns={'dc':xmlns_dc,'dcterms':xmlns_dcterms,'cp':xmlns_cp}

		# Buscamos los metadatos en core.xml
		creator=doc.xpath('//dc:creator',namespaces=ns)
		if len(creator)>0:
			creator=unidecode.unidecode(unicode(creator[0].text))
		else:
			creator='#'
	
		lastModifiedBy=doc.xpath('//cp:lastModifiedBy',namespaces=ns)
		if len(lastModifiedBy)>0:
			lastModifiedBy=unidecode.unidecode(unicode(lastModifiedBy[0].text))
		else:
			lastModifiedBy='#'
	
		created=doc.xpath('//dcterms:created',namespaces=ns)
		if len(created)>0:
			created=unidecode.unidecode(unicode(created[0].text))
		else:
			created='#'

		modified=doc.xpath('//dcterms:modified',namespaces=ns)
		if len(modified)>0:
			modified=unidecode.unidecode(unicode(modified[0].text))
		else:
			modified='#'

		title=doc.xpath('//dc:title',namespaces=ns)
		if len(title)>0:

			title=unidecode.unidecode(unicode(title[0].text))
		else:
			title='#'

		revision=doc.xpath('//cp:revision',namespaces=ns)
		if len(revision)>0:
			revision=unidecode.unidecode(unicode(revision[0].text))
		else:
			revision='#'

		lastPrinted=doc.xpath('//cp:lastPrinted',namespaces=ns)
		if len(lastPrinted)>0:
			lastPrinted=unidecode.unidecode(unicode(lastPrinted[0].text))
		else:
			lastPrinted='#'
		
		keywords=doc.xpath('//cp:keywords',namespaces=ns)
		if len(keywords)>0:
			keywords=unidecode.unidecode(unicode(keywords[0].text))
		else:
			keywords='#'

		#Analizamos el fichero app.xml y sacamos metadatos de ahi.

		app_xml=zf.read('docProps/app.xml')

		#print app_xml

		Aplicacion=re.findall(r'<Application>.*</Application>',app_xml)

		if len(Aplicacion)>0:
			Aplicacion=Aplicacion[0].split('>')[1].split('<')[0]
		else:
			Aplicacion='#'

		Paginas=re.findall(r'<Pages>.*</Pages>',app_xml)

		if len(Paginas)>0:
			Paginas=Paginas[0].split('>')[1].split('<')[0]
		else:
			Paginas='#'

		Palabras=re.findall(r'<Words>.*</Words>',app_xml)

		if len(Palabras)>0:
			Palabras=Palabras[0].split('>')[1].split('<')[0]
		else:
			Palabras='#'

		Caracteres=re.findall(r'<Characters>.*</Characters>',app_xml)

		if len(Caracteres)>0:
			Caracteres=Caracteres[0].split('>')[1].split('<')[0]
		else:
			Caracteres='#'

		Lineas=re.findall(r'<Lines>.*</Lines>',app_xml)

		if len(Lineas)>0:
			Lineas=Lineas[0].split('>')[1].split('<')[0]
		else:
			Lineas='#'


		Parrafos=re.findall(r'<Paragraphs>.*</Paragraphs>',app_xml)

		if len(Parrafos)>0:
			Parrafos=Parrafos[0].split('>')[1].split('<')[0]
		else:
			Parrafos='#'

		Slides=re.findall(r'<Slides>.*</Slides>',app_xml)

		if len(Slides)>0:
			Slides=Slides[0].split('>')[1].split('<')[0]
		else:
			Slides='#'


		PresentationFormat=re.findall(r'<PresentationFormat>.*</PresentationFormat>',app_xml)

		if len(PresentationFormat)>0:
			PresentationFormat=PresentationFormat[0].split('>')[1].split('<')[0]
		else:
			PresentationFormat='#'

		res={
			'Fichero':fichero,
			'Tipo':ext,
			'creator':creator,
			'lastModifiedBy':lastModifiedBy,
			'created':created,
			'modified':modified,
			'title':title,
			'revision':revision,
			'lastPrinted':lastPrinted,
			'keywords':keywords,
			'Application':Aplicacion,
			'Paginas':Paginas,
			'Palabras':Palabras,
			'Caracteres':Caracteres,
			'Lineas':Lineas,
			'Parrafos':Parrafos,
			'Slides':Slides,
			'PresentationFormat':PresentationFormat
		}

		return res


def generar_meta_csv(ruta,output):
	#wkd=os.getcwd()
	#os.chdir(ruta)

	df=pd.DataFrame({'Fichero':[],'Tipo':[],'Creator':[],'LastModifiedBy':[],'Created':[],'Modified':[],'Title':[],'Revision':[],'LastPrinted':[],'Keywords':[],'Application':[],'Paginas':[],'Palabras':[],'Caracteres':[],'Lineas':[],'Parrafos':[],'Slides':[],'PresentationFormat':[],'Producer':[],'Company':[],'Comments':[],'SourceModified':[],'Subject':[]})

	df=df[['Fichero','Tipo','Creator','LastModifiedBy','Created','Modified','Title','Revision','LastPrinted','Keywords','Application','Paginas','Palabras','Caracteres','Lineas','Parrafos','Slides','PresentationFormat','Producer','Company','Comments','SourceModified','Subject']]

	index=0

	for r,d,f in os.walk(ruta):	
		for a in f:
			if r == ruta:    # A partir de aqui hay que extraer metadatos para cada fichero.
				fich=os.path.join(r,a)
				if 'PDF' in magic.from_file(fich):
					print "Es un fichero PDF"
					meta=analizar_file(fich)
					
					if meta=={}:
						continue
					
					df.loc[index]=[meta['Fichero'],meta['Tipo'],meta['Author'],'#',meta['CreationDate'],meta['ModDate'],meta['Title'],'#','#',meta['Keywords'],meta['Creator'],'#','#','#','#','#','#','#',meta['Producer'],meta['Company'],meta['Comments'],meta['SourceModified'],meta['Subject']]
					index=index+1
					continue		

				if fich.split('.')[-1]=='doc' or fich.split('.')[-1]=='xls' or fich.split('.')[-1]=='ppt':
					print "Es un fichero Office antiguo"
					meta=analizar_file(fich)
					
					df.loc[index]=[meta['Fichero'],meta['Tipo'],meta['creator'],meta['lastModifiedBy'],meta['created'],meta['modified'],meta['title'],meta['revision'],meta['lastPrinted'],'#',meta['Application'],meta['Paginas'],meta['Palabras'],meta['Caracteres'],'#','#','#','#','#','#','#','#','#']
					index=index+1
					continue
			

				if 'Word' in magic.from_file(fich):
					if fich.split('.')[-1]!='docx':
						continue
					print "Es un fichero Word"
					meta=analizar_file(fich)

					if meta=={}:
						continue

					df.loc[index]=[meta['Fichero'],meta['Tipo'],meta['creator'],meta['lastModifiedBy'],meta['created'],meta['modified'],meta['title'],meta['revision'],meta['lastPrinted'],meta['keywords'],meta['Application'],meta['Paginas'],meta['Palabras'],meta['Caracteres'],meta['Lineas'],meta['Parrafos'],meta['Slides'],meta['PresentationFormat'],'#','#','#','#','#']
										
					index=index+1
					continue

				if 'Excel' in magic.from_file(fich):
					if fich.split('.')[-1]!='xlsx':
						continue
					print "Es un fichero Excel"
					meta=analizar_file(fich)

					if meta=={}:
						continue
					df.loc[index]=[meta['Fichero'],meta['Tipo'],meta['creator'],meta['lastModifiedBy'],meta['created'],meta['modified'],meta['title'],meta['revision'],meta['lastPrinted'],meta['keywords'],meta['Application'],meta['Paginas'],meta['Palabras'],meta['Caracteres'],meta['Lineas'],meta['Parrafos'],meta['Slides'],meta['PresentationFormat'],'#','#','#','#','#']
					index=index+1
					continue

				if 'PowerPoint' in magic.from_file(fich):
					if fich.split('.')[-1]!='pptx':
						continue
					print "Es un fichero PowerPoint"
					meta=analizar_file(fich)

					if meta=={}:
						continue
					df.loc[index]=[meta['Fichero'],meta['Tipo'],meta['creator'],meta['lastModifiedBy'],meta['created'],meta['modified'],meta['title'],meta['revision'],meta['lastPrinted'],meta['keywords'],meta['Application'],meta['Paginas'],meta['Palabras'],meta['Caracteres'],meta['Lineas'],meta['Parrafos'],meta['Slides'],meta['PresentationFormat'],'#','#','#','#','#']			
					index=index+1
					continue


	df.to_csv(output,header=True,index=False,mode='w',encoding='utf-8')

	documentar={}

	documentar['tipo']=list(df['Tipo'])

	documentar['tipo']=[x.lower() for x in documentar['tipo']] # Pasar los tipos de documentos a minusculas para un mejor procesado a la hora de generar el reporte


	documentar['usuarios']=list(df['Creator'])

	documentar['usuarios'].extend(list(df['LastModifiedBy']))

	documentar['software']=list(df['Application'])

	documentar['software'].extend(list(df['Producer']))

	return documentar



def generate_report(d):


	documentos=['pdf','docx','doc','pptx','ppt','xlsx','xls']

	eje_y=[0]*7

	eje_y[0]=d['tipo'].count('pdf')
	eje_y[1]=d['tipo'].count('docx')
	eje_y[2]=d['tipo'].count('doc')
	eje_y[3]=d['tipo'].count('pptx')
	eje_y[4]=d['tipo'].count('ppt')
	eje_y[5]=d['tipo'].count('xlsx')
	eje_y[6]=d['tipo'].count('xls')


	eje_x=list(range(1,8))

	fig=plt.figure(figsize=(6,2),frameon=False)
	fig.canvas.set_window_title("Reporte metadatos")

	f1=fig.add_subplot(121)
	f1.set_title("Tipos de documentos (bar)",color='k',fontsize=6)

	plt.xticks(eje_x,documentos,fontsize=5)

	xlocs,xlabs= plt.xticks()

	for i,v in enumerate(eje_y):
		plt.text(xlocs[i]-0.2,v + 0.05,str(v),color='b')

	f1.bar(eje_x,eje_y,color='k')

	f2=fig.add_subplot(122)
	f2.set_title("Tipos de documentos (pie)",color='k',fontsize=6)

	f2.pie(eje_y,autopct='%.1f',labels=documentos,shadow=True,explode=[0.08]*7)

	#plt.show()
	f_a='documentos.png'
	fig.savefig(f_a,bbox_inches='tight')


#############################################################

	valores=d['usuarios']
	valores_top10_usuarios=[]
	cantidades_top10=[]

	while len(valores)>0:
		cant=valores.count(valores[0])
		cantidades_top10.append(cant)
		valores_top10_usuarios.append(valores[0])
		valores=[x for x in valores if x!=valores[0]]


	# mapeamos en tuplas los valores de usuarios con sus respectivas apariciones (resultante:una lista de tuplas)
	merged_list_usuarios=[(cantidades_top10[i],valores_top10_usuarios[i]) for i in range(0,len(valores_top10_usuarios))]

	merged_list_usuarios.sort(reverse=True)

	y2=[x[0] for x in merged_list_usuarios]

	x2=[x[1] for x in merged_list_usuarios]

	if len(y2) >=10: # Se puede hacer un top-10 de usuarios
		eje_y2=y2[0:10]
		eje_x2=list(range(1,11))
		usuarios=x2[0:10]

	else:  # Si no, se muestran las apariciones de todos los usuarios que haya
		eje_y2=y2[0:len(y2)]
		eje_x2=list(range(1,len(y2)+1))
		usuarios=x2[0:len(x2)]

	# Ya podemos representar con matplotlib un bar top-10, o todos los usuarios

	fig2=plt.figure(figsize=(6,2),frameon=False)
	fig2.canvas.set_window_title("TOP 10 Usuarios")

	f3=fig2.add_subplot(111)
	f3.set_title("Top 10 metadatos:usuarios",color='k',fontsize=6)

	plt.xticks(eje_x2,usuarios,rotation=15,fontsize=5)

	xlocs,xlabs= plt.xticks()

	
	for i,v in enumerate(eje_y2):
		plt.text(xlocs[i]-0.2,v + 0.05,str(v),color='b')


	f3.bar(eje_x2,eje_y2,color='k')

	#plt.show()
	f_b='top10users.png'
	fig2.savefig(f_b,bbox_inches='tight')

##############################################################

	valores=d['software']
	valores_top10_software=[]
	cantidades_top10=[]

	while len(valores)>0:
		cant=valores.count(valores[0])
		cantidades_top10.append(cant)
		valores_top10_software.append(valores[0])
		valores=[x for x in valores if x!=valores[0]]


	# mapeamos en tuplas los valores de usuarios con sus respectivas apariciones (resultante:una lista de tuplas)
	merged_list_software=[(cantidades_top10[i],valores_top10_software[i]) for i in range(0,len(valores_top10_software))]

	merged_list_software.sort(reverse=True)

	y3=[x[0] for x in merged_list_software]
	x3=[x[1] for x in merged_list_software]

	if len(y3) >=10: # Se puede hacer un top-10 de usuarios
		eje_y3=y3[0:10]
		eje_x3=list(range(1,11))
		software=x3[0:10]

	else:  # Si no, se muestran las apariciones de todos los usuarios que haya
		eje_y3=y3[0:len(y3)]
		eje_x3=list(range(1,len(y3)+1))
		software=x3[0:len(x3)]

	# Ya podemos representar con matplotlib un bar top-10, o todos los usuarios

	fig3=plt.figure(figsize=(6,2),frameon=False)
	fig3.canvas.set_window_title("TOP 10 Software")

	f4=fig3.add_subplot(111)
	f4.set_title("Top 10 metadatos:Software",color='k',fontsize=6)

	plt.xticks(eje_x3,software,rotation=15,fontsize=5)

	xlocs,xlabs= plt.xticks()

	for i,v in enumerate(eje_y3):
		plt.text(xlocs[i]-0.2,v + 0.05,str(v),color='b')

	f4.bar(eje_x3,eje_y3,color='k')

	#plt.show()
	f_c='top10software.png'
	fig3.savefig(f_c,bbox_inches='tight')

#############################################################3

	pdf = FPDF(orientation='P',unit='mm',format='A4')
	pdf.set_auto_page_break(False,margin=0.0)
	pdf.add_page()
	pdf.set_xy(0, 0)
	pdf.set_font('arial', 'B', 18)
	pdf.cell(60,100)
	pdf.cell(75, 10, "REPORTE DE METADATOS (USUARIOS Y SOFTWARE)", 0, 2, 'C')
	pdf.cell(90, 10, " SAMIR KAMAL MORENO ", 0, 2, 'C')
	#pdf.cell(-40)
	#pdf.line(0,120,90,120)
	pdf.cell(90, 10, " ", 0, 2, 'C')
	pdf.image(f_a, x = 0, y = None, w = 0, h = 0, type = '', link = '')
	pdf.cell(90, 15, " ", 0, 2, 'C')
	pdf.image(f_b, x = 0, y = None, w = 0, h = 0, type = '', link = '')
	#pdf.cell(90, 15, " ", 0, 2, 'C')
	pdf.image(f_c, x = 0, y = None, w = 0, h = 0, type = '', link = '')
	pdf.output('report.pdf', 'F')





if __name__=="__main__":
	#r=analizar_file('/root/Desktop/bitacora/vas.pptx')
	#print r

	#r=analizar_file('/root/Escritorio/bitas/Carta_CGT.doc')
	#print r

	#r=analizar_file('/root/Escritorio/bitas/nop.ppt')
	#print r

	doc=generar_meta_csv('/root/Escritorio/Descargas','resultados.csv')
	generate_report(doc)	

	#print doc











