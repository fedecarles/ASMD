#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import re
from cookielib import CookieJar
import time
import datetime
import sqlite3
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

conn = sqlite3.connect("/home/fedecarles/asmd/ASMD.db")
conn.text_factory = str
c = conn.cursor()

negativeWords = []
positiveWords = []
neutralWords = []
allKeyWords = []
adj_query = "SELECT * FROM adjetivos WHERE valor =?"


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

def lanacion_scraper():
    try:
        page = "http://contenidos.lanacion.com.ar/herramientas/rss-categoria_id=30"
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link href="(.*?)" />', sourceCode)
            print(links)
            for link in links:
                linkSource = opener.open(link).read()
                linkSource = re.sub('\s+', ' ', linkSource).strip()
                currentTime = time.time()
                dateStamp = datetime.datetime.fromtimestamp(currentTime)\
                    .strftime('%Y-%m-%d')
                fuente = "LA NACION"
                titulo = re.findall(r'<title>(.*?)</title>', linkSource)
                linesOfInterest = re.findall(r'<p>(.*?)</p>',
                                             str(linkSource))
                valor = []

                for lines in linesOfInterest:
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
                                          (link, titulo[0], valor, fuente,
                                           currentTime, dateStamp, eachEnt,
                                           eachDesc))
                                conn.commit()

        except Exception:
            print "Error en 2do intento"
    except Exception:
        print "Error en primer intento"

def clarin_scraper():
    try:
        page = 'http://www.clarin.com/rss/politica/'
        sourceCode = opener.open(page).read()
        print type(sourceCode)
        try:
            links = re.findall(r'<link>(.*?html)</link>', sourceCode)
            print(links)
            for link in links:
                linkSource = opener.open(link).read()
                linkSource = re.sub('\s+', ' ', linkSource).strip()

                currentTime = time.time()
                dateStamp = datetime.datetime.fromtimestamp(currentTime)\
                    .strftime('%Y-%m-%d')
                fuente = "CLARIN"
                titulo = re.findall(r'<title>(.*?)</title>', linkSource)
                valor = []

                linesOfInterest = re.findall(r'<div class="nota">(.*?)</div>',
                                             str(linkSource))
                for lines in linesOfInterest:
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
                                          (link, titulo[0], valor, fuente,
                                           currentTime, dateStamp, eachEnt,
                                           eachDesc))
                                conn.commit()

        except Exception:
            print "Error en segundo intento"
    except Exception:
        print "Error en primer intento"

def infobae_scraper():
    try:
        page = 'http://cdn01.ib.infobae.com/adjuntos/162/rss/politica.xml'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>',
                               sourceCode.decode('utf-8'))
            del links[0:2]
            for link in links:
                linkSource = opener.open(link).read()
                linkSource = re.sub('\s+', ' ', linkSource).strip()
                currentTime = time.time()
                dateStamp = datetime.datetime.fromtimestamp(currentTime)\
                    .strftime('%Y-%m-%d')
                fuente = "INFOBAE"
                titulo = re.findall(r'<title>(.*?)</title>',
                                    linkSource.decode('utf-8'))
                valor = []

                linesOfInterest = re.findall(r'description":(.*?)","articleSection"',
                                             str(linkSource).decode('utf-8'))
                for lines in linesOfInterest:
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
                                          (link, titulo[0], valor, fuente,
                                           currentTime, dateStamp, eachEnt,
                                           eachDesc))
                                conn.commit()

        except Exception, e:
            print str(e)
            print "Error en 2do intento"
    except Exception:
        print "Error en 1er intento"

def pagina12_scraper():
    try:
        page = 'http://www.pagina12.com.ar/diario/rss/ultimas_noticias.xml'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link>(.*?)</link>',
                               sourceCode.decode('iso-8859-1'))
            del links[0:2]
            print links
            for link in links:
                linkSource = opener.open(link).read()
                linkSource = re.sub('\s+', ' ', linkSource).strip()
                currentTime = time.time()
                dateStamp = datetime.datetime.fromtimestamp(currentTime)\
                    .strftime('%Y-%m-%d')
                fuente = "PAGINA 12"
                titulo = re.findall(r'Ultimas Noticias :: (.*?)<\/title>',
                                    linkSource.decode('iso-8859-1'))
                valor = []

                linesOfInterest = re.findall(r'<div id="cuerpo"><p class="margen0">(.*?)<script type="text/javascript">',
                                             str(linkSource))
                for lines in linesOfInterest:
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
                                          (link, titulo[0], valor, fuente,
                                           currentTime, dateStamp, eachEnt,
                                           eachDesc))
                                conn.commit()

        except Exception, e:
            print str(e)
            print "Error en 2do intento"
    except Exception:
        print "Error en 1er intento"

pagina12_scraper()

def removeJunk():
    junkWords = ["LA NACION", "Infobae TV"]
    for junk in junkWords:
        c.execute("DELETE FROM entidades WHERE entidad =?", [(junk)])
        conn.commit()
removeJunk()


