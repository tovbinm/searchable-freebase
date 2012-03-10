'''
Created on Feb 19, 2011

@author: matthew
'''
import webUtils
import os
import csv

class _dataUtils:
    def downloadData(self, db_dir_url, data_dir):
        print 'Downloading data...'
        
        wu = webUtils._webUtils()
        print 'Listing contents of ' + db_dir_url
        
        items = wu.getDirItems(db_dir_url)
        for item in items:
            print 'Downloading contents of ' + db_dir_url + item
            itemData = wu.getContent(db_dir_url + item)
            f = open(data_dir + item, 'w')
            f.write(itemData)
            f.close()
            print 'Saved to ' + data_dir + item
            
        print 'Data downloaded.'
        
    def storeData(self, data_dir, dataProvider):
        print 'Storing data...'
        print 'Listing data files from ' + data_dir
        
        dataFilesNames = []
        dataFiles = os.listdir(data_dir)
        for dataFile in dataFiles:
            print 'Reading data file ' + data_dir + dataFile
            f = open(data_dir + dataFile, 'r')
            try:
                dataReader = csv.reader(f, delimiter='\t')          
                dfName = getDataFileNameOnly(dataFile);     
                dataProvider.storeNodes(dataReader, dfName) 
                dataFilesNames.append(dfName)          
            finally:
                f.close()
        dataProvider.dataFiles = dataFilesNames
        dataProvider.storeRelations()
        print 'Data store completed.'
    
def getDataFileNameOnly(dataFile):
    return dataFile.replace('.tsv','')
