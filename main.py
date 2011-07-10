'''
Created on Feb 19, 2011

@author: matthew
'''

import dataUtils
import os
import sys
import const
import utils
import data.dataProviderFactory
import pprint
import shutil


if __name__ == '__main__':
    agrvDic = utils.list2Dict(sys.argv)
     
    const.db_dir_url = "http://download.freebase.com/datadumps/latest/browse/games/"
    const.data_dir =  os.path.curdir + '/dataFiles/'    
    #const.db_path = 'http://localhost:7474/db/data/'
    const.db_path = os.path.curdir+'/db/data' 
    
    ##### Init data utils and providers #####
    du = dataUtils._dataUtils()
    dpf = data.dataProviderFactory._dataProviderFactory()
    if (agrvDic.__contains__('-store')): shutil.rmtree(const.db_path, ignore_errors=True)     
    dpParams = {'dbPath' : const.db_path,'dataFiles': []};
    if os.path.exists(const.data_dir):
        dpParams.__setitem__('dataFiles', os.listdir(const.data_dir))                   
    dataProvider = dpf.getDataProvider('neo4j', dpParams)
    
    
    ###### Parsing arguments ########
    if (agrvDic.__contains__('-download')):
        if not os.path.exists(const.data_dir):
            os.mkdir(const.data_dir)
        du.downloadData(const.db_dir_url, const.data_dir)  
   
    if (agrvDic.__contains__('-store')):
        if not os.path.exists(const.data_dir) or os.listdir(const.data_dir) == []:
            print 'Please download data first. Use "-download" argument'
            sys.exit()  
                    
        du.storeData(const.data_dir, dataProvider)         
   
              
    if (agrvDic.__contains__('-query')):        
        dummy = True  
        print '\n'
        while dummy == True:          
            i = 0
            for df in dataProvider.dataFiles:        
                print str(i)+') '+dataUtils.getDataFileNameOnly(df)
                i = i + 1
            q = raw_input("Please choose one of the above indexes (enter 0-"+str((len(dataProvider.dataFiles)-1))+"): ")
            try: num = int(q) 
            except: continue
            if (num >=0 and num < len(dataProvider.dataFiles)):
                dataFile = dataProvider.dataFiles[num]
                print "Index '"+dataFile+"' was chosen.\n"
                break  
        pprintr = pprint.PrettyPrinter(indent=4)       
        while dummy == True:
            q = raw_input("\nPlease enter your query (or type 'quit;' to quit):")            
            if (q == 'quit;') : break
            q = q.strip()
            if (q == None or len(q)==0) : continue
                    
            results = dataProvider.getNode(dataFile, q)
            if results == None or results == []:
                print 'No results'
            else:
                for res in results:
                    pprintr.pprint(res)
                print 'Found '+str(len(results))+' results matching your criteria.'
    
    dataProvider.cleanUp();
    print 'Bye.'
