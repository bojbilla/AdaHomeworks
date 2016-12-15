import json
import numpy as np
import pandas as pd
from wordcloud import WordCloud as wc
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk import WordNetLemmatizer as wnl
import nltk
import re
import pycountry as pc
from PIL import Image
from os import path
from nltk.sentiment import SentimentIntensityAnalyzer as st
from nltk.stem import WordNetLemmatizer

def cloud(text): 
    """ Generate wordcloud """
    text = ' '.join(text) if type(text) != str else text
    wordcloud = wc(max_font_size=80, stopwords=[""], width=500, height=250, background_color='White').generate(text)
    plt.figure(figsize=(10,50))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
	
def usa_cloud(text):
    """ Generate wordcloud """
    text = ' '.join(text) if type(text) != str else text
    usa_mask = np.array(Image.open(path.join(path.dirname(__file__), "usa_map.jpg")))
    wordcloud = wc(max_font_size=80, stopwords=[""], width=500, height=250, background_color='White', mask=usa_mask).generate(text)
    plt.figure(figsize=(10,50))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
def write(my_dict, name):
    """ Write to json """
    json.dump(my_dict, open(name+".json",'w'))

    
def read(name):
    """ Read from json """
    return json.load(open(name+".json"))
	
def preprocess_raw_email(text):
	"""Very simple email preprocessing that tries to remove
	email protocol metadata and standard headers"""

	keywords = ('U.S. Department of State', 'Department of State', 'Case No.',
				'Doc No.', 'STATE DEPT.', 'UNCLASSIFIED',
				'From:', 'To:', 'Sent:', 'Subject:', 'Attachments:',
				'Date:', 'Cc:', 'SUBJECT TO AGREEMENT ON SENSITIVE INFORMATION & REDACTIONS',
				'NO FOIA WAIVER','RELEASE IN FULL', 'UNCLASSIFIED')

	# Remove lines starting with keyword
	lines = text.split('\n')
	ls = []
	for l in lines:
		put = True
		for k in keywords:
			if(k in l):
				put = False
				break
		if(put == True):
			ls.append(l)
		
	return '\n'.join(ls)