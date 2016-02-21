#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapers_test import Scraper, removeJunk

sc = Scraper()
sc.scrapeInfobae("http://cdn01.ib.infobae.com/adjuntos/162/rss/politica.xml")
sc.scrapeLaNacion("http://contenidos.lanacion.com.ar/herramientas/rss-categoria_id=30")
sc.scrapeClarin("http://www.clarin.com/rss/politica/")
sc.scrapePagina12("http://www.pagina12.com.ar/diario/rss/ultimas_noticias.xml")
sc.scrapePerfil("http://www.perfil.com/rss/politica.xml")
sc.scrapeInfonews("http://www.infonews.com/rss/politica.xml")
sc.scrapeMendozaOnline("http://www.mdzol.com/files/rss/politica.xml")
sc.scrapeTelam("http://www.telam.com.ar/rss2/politica.xml")
sc.scrapeLosAndes("http://losandes.com.ar/rss/politica")
sc.scrapeLaVoz("http://www.lavoz.com.ar/taxonomy/term/4/1/feed")


removeJunk()
