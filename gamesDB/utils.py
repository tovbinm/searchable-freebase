'''
Created on Feb 19, 2011

@author: matthew
'''
import unicodedata

def list2Dict(lst):
    dic = {}
    for item in lst:
        dic[item] = item 
    return dic

def remove_accents(str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(str))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii