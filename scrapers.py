#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import re
from cookielib import CookieJar
import time
import datetime
import sqlite3
import sys
import HTMLParser

reload(sys)
sys.setdefaultencoding('utf8')

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

### Carga la base de datos
conn = sqlite3.connect("/home/fedecarles/asmd/ASMD.db")
conn.text_factory = str
c = conn.cursor()

negativeWords = []
positiveWords = []
neutralWords = []
allKeyWords = []
adj_query = "SELECT * FROM adjetivos WHERE valor =?"
vis_query = "SELECT link FROM entidades"
# HTML parser para escapar la conversión html de caracteres non-ascii
pars = HTMLParser.HTMLParser()


### función para cargar las palabras asociadas
def loadWordArrays():
    for negRow in c.execute(adj_query, [(-1)]):
        negativeWords.append(negRow[0])
        allKeyWords.append(negRow[0])

    for posRow in c.execute(adj_query, [(1)]):
        positiveWords.append(posRow[0])
        allKeyWords.append(posRow[0])

    for neuRow in c.execute(adj_query, [(0)]):
        neutralWords.append(neuRow[0])
        allKeyWords.append(neuRow[0])

loadWordArrays()

### función para cargar los links visitados
visitedLinks = []
def loadVisitedLinks():
    for link in c.execute(vis_query):
        visitedLinks.append(link[0])

loadVisitedLinks()

# La clase scraper tiene 3 funciones separadas para la extracción de
# las entidades y carga en la base de datos. Las 3 funciones getEntities
# son para manejar los diferentes encodings (utf-8, iso-8859-1, uescape).

# El resto de las funciones de la clase son son específicas a cada sitio de
# noticias. Extraen las urls, títulos, y cuerpo de la nota, que son
# procesados con las funciones getEntities.


class Scraper:

    def __init__(self):

        self.currentTime = time.time()
        self.dateStamp = (datetime.datetime.fromtimestamp(self.currentTime)
                     .strftime('%Y-%m-%d'))

    def getEntities_uescape(self, text):
        for lines in text:
            sent_split = lines.split(".")
            for sent in sent_split:
                entidad = re.findall(ur"([A-Z][a-zA-Záéíñóú]+(?=\s[A-Z])(?:\s[A-Z][a-zA-Záéíñóú]+)+)",
                                 sent.decode('unicode-escape'))
                if len(entidad) > 1:
                    pass
                elif len(entidad) == 0:
                    pass
                else:
                    print entidad
                    word_split = sent.split()
                    descriptives = []
                    for word in word_split:
                        if word in allKeyWords:
                            descriptives.append(word)

                    for eachEnt in entidad:
                        eachEnt.replace(',', '').replace('.', '').encode('utf-8')

                    for eachDesc in descriptives:
                        print eachDesc
                        eachDesc.lower().encode('utf-8')
                        if eachDesc in positiveWords:
                            valor = 1
                        elif eachDesc in negativeWords:
                            valor = -1
                        else:
                            valor = 0
                        c.execute("""INSERT INTO entidades(link, titulo,
                                           valor, fuente, unix, dateStamp, entidad,
                                           adjetivo) VALUES(?,?,?,?,?,?,?,?)""",
                                           (self.link, self.titulo[0], valor, self.fuente,
                                            self.currentTime, self.dateStamp, eachEnt,
                                            eachDesc))
                        conn.commit()

    def getEntities_utf(self, text):
        for lines in text:
            sent_split = lines.split(".")
            for sent in sent_split:
                entidad = re.findall(ur"([A-Z][a-zA-Záéíñóú]+(?=\s[A-Z])(?:\s[A-Z][a-zA-Záéíñóú]+)+)",
                                 sent.decode('utf-8'))
                if len(entidad) > 1:
                    pass
                elif len(entidad) == 0:
                    pass
                else:
                    print entidad
                    word_split = sent.split()
                    descriptives = []
                    for word in word_split:
                        if word in allKeyWords:
                            descriptives.append(word)

                    for eachEnt in entidad:
                        eachEnt.replace(',', '').replace('.', '').encode('utf-8')

                    for eachDesc in descriptives:
                        print eachDesc
                        eachDesc.lower().encode('utf-8')
                        if eachDesc in positiveWords:
                            valor = 1
                        elif eachDesc in negativeWords:
                            valor = -1
                        else:
                            valor = 0
                        c.execute("""INSERT INTO entidades(link, titulo,
                                           valor, fuente, unix, dateStamp, entidad,
                                           adjetivo) VALUES(?,?,?,?,?,?,?,?)""",
                                           (self.link, self.titulo[0], valor, self.fuente,
                                            self.currentTime, self.dateStamp, eachEnt,
                                            eachDesc))
                        conn.commit()

    def getEntities_iso(self, text):
        for lines in text:
            sent_split = lines.split(".")
            for sent in sent_split:
                entidad = re.findall(ur"([A-Z][a-zA-Záéíñóú]+(?=\s[A-Z])(?:\s[A-Z][a-zA-Záéíñóú]+)+)",
                                 sent.decode('iso-8859-1'))
                if len(entidad) > 1:
                    pass
                elif len(entidad) == 0:
                    pass
                else:
                    print entidad
                    word_split = sent.split()
                    descriptives = []
                    for word in word_split:
                        if word in allKeyWords:
                            descriptives.append(word)

                    for eachEnt in entidad:
                        eachEnt.replace(',', '').replace('.', '').encode('utf-8')

                    for eachDesc in descriptives:
                        print eachDesc
                        eachDesc.lower().encode('utf-8')
                        if eachDesc in positiveWords:
                            valor = 1
                        elif eachDesc in negativeWords:
                            valor = -1
                        else:
                            valor = 0
                        c.execute("""INSERT INTO entidades(link, titulo,
                                           valor, fuente, unix, dateStamp, entidad,
                                           adjetivo) VALUES(?,?,?,?,?,?,?,?)""",
                                           (self.link, self.titulo[0], valor, self.fuente,
                                            self.currentTime, self.dateStamp, eachEnt,
                                            eachDesc))
                        conn.commit()

    def scrapeInfobae(self, url):
        try:
            self.page = url
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(.*?)</link>',
                                    self.sourceCode.decode('utf-8'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "INFOBAE"
                    self.titulo = re.findall(r'<title>(.*?)</title>',
                                             self.linkSource.decode('utf-8'))

                    self.linesOfInterest = re.findall(r'description":(.*?)","articleSection"',
                                                      str(self.linkSource).decode('utf-8'))
                    self.getEntities_uescape(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

    def scrapeLaNacion(self, url):
        try:
            self.page = url
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link href="(.*?)" />',
                                    self.sourceCode.decode('utf-8'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "LA NACION"
                    self.titulo = re.findall(r'<title>(.*?)</title>',
                                             self.linkSource.decode('utf-8'))

                    self.linesOfInterest = re.findall(r'<p>(.*?)</p>',
                                                      str(self.linkSource).decode('utf-8'))
                    self.getEntities_utf(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

    def scrapeClarin(self, url):
        try:
            self.page = url
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(.*?html)</link>',
                                    self.sourceCode.decode('utf-8'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "CLARIN"
                    self.titulo = re.findall(r'<title>(.*?)</title>',
                                             self.linkSource.decode('utf-8'))

                    self.linesOfInterest = re.findall(r'<div class="nota">(.*?)</div>',
                                                      str(self.linkSource).decode('utf-8'))
                    self.getEntities_utf(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

    def scrapePagina12(self, url):
        try:
            self.page = url
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(.*?)</link>',
                                    self.sourceCode.decode('iso-8859-1'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "PAGINA 12"
                    self.titulo = re.findall(r'Ultimas Noticias :: (.*?)<\/title>',
                                             self.linkSource.decode('iso-8859-1'))

                    self.linesOfInterest = re.findall(r'<div id="cuerpo"><p class="margen0">(.*?)<script type="text/javascript">',
                                                      str(self.linkSource))
                    self.getEntities_iso(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

    def scrapePerfil(self, url):
        try:
            self.page = url
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(http://www.perfil.com/.*?)</link>',
                                    self.sourceCode.decode('utf-8'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "PERFIL"
                    self.titulo = re.findall(r'<title>(.*?)</title>',
                                             self.linkSource.decode('utf-8'))

                    self.linesOfInterest = re.findall(r'<div itemprop="articleBody"><p>(.*?)</section>',
                                                      str(self.linkSource))
                    self.linesOfInterest = [pars.unescape(i) for i in self.linesOfInterest]
                    self.getEntities_utf(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

    def scrapeInfonews(self, url):
        try:
            self.page = url
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(http://www.infonews.com/nota/.*?)</link>',
                                    self.sourceCode.decode('utf-8'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "INFONEWS"
                    self.titulo = re.findall(r'<title>(.*?)| Política | INFOnews</title>',
                                             self.linkSource.decode('utf-8'))
                    self.titulo = [pars.unescape(i) for i in self.titulo]
                    self.linesOfInterest = re.findall(r'<div itemprop="articleBody" class="article-body">(.*?)div class="article-comments"',
                                                      str(self.linkSource))
                    self.linesOfInterest = [pars.unescape(i) for i in self.linesOfInterest]
                    self.getEntities_utf(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

    def scrapeMendozaOnline(self, url):
        try:
            self.page = url
            print self.page
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(http://www.mdzol.com/nota/.*?)</link>',
                                    self.sourceCode.decode('utf-8'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "MENDOZA ONLINE"
                    self.titulo = re.findall(r'<title>(.*?)</title>',
                                             self.linkSource.decode('utf-8'))
                    self.linesOfInterest = re.findall(r'id=vsmcontent>(.*?)id=rating-wrapper><script>',
                                                      str(self.linkSource))
                    self.getEntities_utf(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

    def scrapeTelam(self, url):
        try:
            self.page = url
            print self.page
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(http://www.telam.com.ar/notas/.*?)</link>',
                                    self.sourceCode.decode('iso-8859-1'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "TELAM"
                    self.titulo = re.findall(r'<title>(.*?)</title>',
                                             self.linkSource.decode('iso-8859-1'))
                    self.titulo = [pars.unescape(i) for i in self.titulo]
                    self.linesOfInterest = re.findall(r'<br />(.*?)<br />',
                                                      str(self.linkSource))
                    self.getEntities_iso(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

    def scrapeLosAndes(self, url):
        try:
            self.page = url
            print self.page
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(http://www.losandes.com.ar/article/.*?)</link>',
                                    self.sourceCode.decode('utf-8'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "LOS ANDES"
                    self.titulo = re.findall(r'<title>(.*?)Los Andes Diario</title>',
                                             self.linkSource.decode('utf-8'))
                    self.linesOfInterest = re.findall(r'<div class="span10">(.*?)</article>',
                                                      str(self.linkSource))
                    self.linesOfInterest = [pars.unescape(i) for i in self.linesOfInterest]
                    self.getEntities_utf(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

    def scrapeLaVoz(self, url):
        try:
            self.page = url
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(http://www.lavoz.com.ar/politica/.*?)</link>',
                                    self.sourceCode.decode('utf-8'))
            for self.link in self.links:
                if self.link in visitedLinks:
                    print "Link ya visitado"
                else:
                    self.linkSource = opener.open(self.link).read()
                    self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                    self.fuente = "LA VOZ"
                    self.titulo = re.findall(r'<title>(.*?)</title>',
                                             self.linkSource.decode('utf-8'))
                    self.linesOfInterest = re.findall(r'<div class="TextoNota"(.*?)<div class="masInfo">',
                                                      str(self.linkSource))
                    self.getEntities_utf(self.linesOfInterest)
        except Exception:
             print "Falló el scraping"

# sc = Scraper()
# sc.scrapeInfobae("http://cdn01.ib.infobae.com/adjuntos/162/rss/politica.xml")
# sc.scrapeLaNacion("http://contenidos.lanacion.com.ar/herramientas/rss-categoria_id=30")
# sc.scrapeClarin("http://www.clarin.com/rss/politica/")
# sc.scrapePagina12("http://www.pagina12.com.ar/diario/rss/ultimas_noticias.xml")
# sc.scrapePerfil("http://www.perfil.com/rss/politica.xml")
# sc.scrapeInfonews("http://www.infonews.com/rss/politica.xml")
# sc.scrapeMendozaOnline("http://www.mdzol.com/files/rss/politica.xml")
# sc.scrapeTelam("http://www.telam.com.ar/rss2/politica.xml")
# sc.scrapeLosAndes("http://losandes.com.ar/rss/politica")
# sc.scrapeLaVoz("http://www.lavoz.com.ar/taxonomy/term/4/1/feed")


def removeJunk():
    junkWords = ["LA NACION", "Infobae TV", "Revista Noticias"]
    for junk in junkWords:
        c.execute("DELETE FROM entidades WHERE entidad =?", [(junk)])
        conn.commit()
