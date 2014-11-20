# -*- coding: utf-8 -*-
"""
Created on Sun Sep 14 16:23:19 2014

@author: Leo
"""
import re
import requests
import string
import time


def song_word_count(artist,song_name):

    artist=artist.lower()
    artist=artist.replace(" ","")
    song_name=song_name.lower()
    song_name=song_name.replace(" ","")
    
    
    url="http://www.azlyrics.com/lyrics/"+artist+"/"+song_name+".html"
    #print url
    response = requests.get(url)
    
    song=re.findall(r'<!-- start of lyrics -->(.*?)<!-- end of lyrics -->',response.content,re.DOTALL)
    
    try:
        song=song[0]
        TAG_RE = re.compile(r'<[^>]+>')
        song=TAG_RE.sub(' ', song)
        TAG_RE = re.compile(r'\n')
        song=TAG_RE.sub(' ', song)
        TAG_RE = re.compile(r'\r')
        song=TAG_RE.sub(' ', song)
        TAG_RE = re.compile(r'\[[^\]]+]')
        song=TAG_RE.sub(' ', song)
        TAG_RE = re.compile(r'\(')
        song=TAG_RE.sub(' ', song)
        TAG_RE = re.compile(r'\)')
        song=TAG_RE.sub(' ', song)
        song=song.lower()
        
        replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
        song = song.translate(replace_punctuation)
        
        song_list=song.split()
        #print song_list
        song_set=set(song_list)
        #print song_set
        
        words=len(song_list)
        unique_words=len(song_set)
        
        return(words,unique_words)
    
    except:
        return(0,0)
    
    #print(words)
    #print(unique_words)
