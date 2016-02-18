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

def wordParser(linesOfInterest):

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
                wordParser(linesOfInterest)


        except Exception, e:
            print str(e)
    except Exception, e:
        print str(e)

lanacion_scraper()
