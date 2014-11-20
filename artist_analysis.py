# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 23:49:29 2014

@author: work
"""

import song_analysis as sa
import re
import requests
import string
import pandas as pdc
import bs4
import time

path = 'C:\\Users\\work\\Documents\\Python_data'
file = os.path.join(path, 'artists.csv')

artist="booba"
genre="rap"

import pandas as pd

artist_url=artist.lower()
artis_url=artist_url.replace(" ","")

url="http://www.azlyrics.com/"+artist[0]+"/"+artist_url+".html"
print url
response = requests.get(url)

soup=bs4.BeautifulSoup(response.text)
links = soup.find(id='listAlbum').findAll('a')

db=pd.DataFrame(columns=['song','album','genre','artist','words','unique_words'])

db = pd.read_csv(file, sep = ';', header = False)

for elem in links:
    time.sleep(2)
    string=str(elem)
    #print(string)
    if string.find('amazon')==-1:
        song_name=str(elem)
        TAG_RE = re.compile(r'<[^>]+>')
        song_name=TAG_RE.sub(' ', song_name)
        TAG_RE = re.compile(r"'")
        song_name=TAG_RE.sub(' ', song_name)
        #replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
        #song_name = song_name.translate(replace_punctuation)        
        
        print 'song name : '+song_name
        (words,unique_words)= sa.song_word_count(artist,song_name)
        
        song_dict = dict(song=song_name, artist=artist, album='', genre=genre, words=words,unique_words=unique_words)
        db=db.append(song_dict, ignore_index=True)
    else:
        links.remove(elem)

db.to_csv(file, sep = ';', index=False)
            
#song_name="yellow submarine"

#sa.song_word_count(artist,song_name)