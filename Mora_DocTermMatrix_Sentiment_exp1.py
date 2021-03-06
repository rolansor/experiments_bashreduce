#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import os
import pandas as pd
import operator
import textmining
from nltk.stem import RegexpStemmer
from stop_words import get_stop_words
from nltk.corpus import stopwords
from good_bad import Adjectives


dictionario = {}
more_stop_en = set(get_stop_words('english'))
more_stop_es = set(get_stop_words('spanish'))
stop_es = set(stopwords.words("spanish"))
stop_en = set(stopwords.words("english"))
adj = Adjectives()
tdm = textmining.TermDocumentMatrix()

room = 0
#for line in var:
for line in sys.stdin:
	room+=1
	line = line.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u');
	line = re.sub('[0-9,#,!,¡,&,.]','',line)
	line = re.sub('[^a-zA-Z]'," ",line)
	words = line.lower().split()
	st = RegexpStemmer('ing$|s$|able$|thing$|ful$', min=4)
	words = [st.stem(w) for w in words]
	words = [w for w in words if not w in stop_en and not w in stop_es]
	words = [w for w in words if not w in more_stop_en and not w in more_stop_es]
	words = [w for w in words if len(w) > 2]
	tdm.add_doc(" ".join(words))


	good_count = [ words.count(ad) for ad in adj.good if ad in words]
	good_count = len(good_count)

	bad_count = [ words.count(ad) for ad in adj.bad if ad in words]
	bad_count = len(bad_count)


	print 'Comentario '+str(room)+': Sentiment Score: '+str(good_count - bad_count)+'\n' 


for row in tdm.rows(cutoff=1):
	print row
		

