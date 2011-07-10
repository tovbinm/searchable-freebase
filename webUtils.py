'''
Created on Feb 19, 2011

@author: matthew
'''

import urllib
import re

class _webUtils:
    
    def getContent(self, url):
        f = urllib.urlopen(url)
        resStr = f.read()
        f.close()
        return resStr
    
    def getDirItems(self, url):
        resStr = self.getContent(url)
        matches = re.findall('alt="\[TXT\]"></td><td><a href="(.*?)">(.*?)</a></td>', resStr);    
        retItems = []
        for match in matches:         
            retItems.append(match[0])
        return retItems