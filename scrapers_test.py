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

conn = sqlite3.connect("NewsMonitor.db")
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


class Scraper:

    def __init__(self):

        self.currentTime = time.time()
        self.dateStamp = (datetime.datetime.fromtimestamp(self.currentTime)
                     .strftime('%Y-%m-%d'))

    def getEntities(self, text):
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


    def getLinks(self, url):
        try:
            self.page = url
            self.sourceCode = opener.open(self.page).read()
            self.links = re.findall(r'<link>(.*?)</link>',
                                    self.sourceCode.decode('utf-8'))
            for self.link in self.links:
                self.linkSource = opener.open(self.link).read()
                self.linkSource = re.sub('\s+', ' ', self.linkSource).strip()
                self.fuente = "INFOBAE"
                self.titulo = re.findall(r'<title>(.*?)</title>',
                                    self.linkSource.decode('utf-8'))

                self.linesOfInterest = re.findall(r'description":(.*?)","articleSection"',
                                              str(self.linkSource).decode('utf-8'))

                self.getEntities(self.linesOfInterest)



        except Exception, e:
            print str(e)



sc = Scraper()
sc.getLinks("http://cdn01.ib.infobae.com/adjuntos/162/rss/politica.xml")



# def infobae_scraper():
#     try:
#         page = 'http://cdn01.ib.infobae.com/adjuntos/162/rss/politica.xml'
#         sourceCode = opener.open(page).read()
#         try:
#             links = re.findall(r'<link>(.*?)</link>',
#                                sourceCode.decode('utf-8'))
#             del links[0:2]
#             for link in links:
#                 linkSource = opener.open(link).read()
#                 linkSource = re.sub('\s+', ' ', linkSource).strip()
#                 currentTime = time.time()
#                 dateStamp = datetime.datetime.fromtimestamp(currentTime)\
#                     .strftime('%Y-%m-%d')
#                 fuente = "INFOBAE"
#                 titulo = re.findall(r'<title>(.*?)</title>',
#                                     linkSource.decode('utf-8'))
#                 valor = []
#
#                 linesOfInterest = re.findall(r'description":(.*?)","articleSection"',
#                                              str(linkSource).decode('utf-8'))
#                 for lines in linesOfInterest:
#                     sent_split = lines.split(".")
#                     for sent in sent_split:
#                         entidad = re.findall(ur"([A-Z][a-zA-Záéíñóú]+(?=\s[A-Z])(?:\s[A-Z][a-zA-Záéíñóú]+)+)",
#                                          sent.decode('unicode-escape'))
#                         if len(entidad) > 1:
#                             pass
#                         elif len(entidad) == 0:
#                             pass
#                         else:
#                             print entidad
#                             word_split = sent.split()
#                             descriptives = []
#                             for word in word_split:
#                                 if word in allKeyWords:
#                                     descriptives.append(word)
#
#                             for eachEnt in entidad:
#                                 eachEnt.replace(',', '').replace('.', '').encode('utf-8')
#
#                             for eachDesc in descriptives:
#                                 print eachDesc
#                                 eachDesc.lower().encode('utf-8')
#                                 if eachDesc in positiveWords:
#                                     valor = 1
#                                 elif eachDesc in negativeWords:
#                                     valor = -1
#                                 else:
#                                     valor = 0
#                                 c.execute("""INSERT INTO entidades(link, titulo,
#                                           valor, fuente, unix, dateStamp, entidad,
#                                           adjetivo) VALUES(?,?,?,?,?,?,?,?)""",
#                                           (link, titulo[0], valor, fuente,
#                                            currentTime, dateStamp, eachEnt,
#                                            eachDesc))
#                                 conn.commit()
#
#         except Exception, e:
#             print str(e)
#             print "Error en 2do intento"
#     except Exception:
#         print "Error en 1er intento"
#


def removeJunk():
    junkWords = ["LA NACION", "Infobae TV"]
    for junk in junkWords:
        c.execute("DELETE FROM entidades WHERE entidad =?", [(junk)])
        conn.commit()
removeJunk()


