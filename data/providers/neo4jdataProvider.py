'''
Created on Feb 19, 2011

@author: matthew
'''

import neo4j
import dataUtils
import data.gamesRelationsMapper
import re
import data.defaultTraverse
import pprint

class neo4jdataProvider:
   
    def __init__(self, params):
        self.dbPath = params["dbPath"]
        self.graphdb = neo4j.GraphDatabase(self.dbPath)         
        self.dataFiles = []
        dfs = params["dataFiles"]
        for df in dfs: self.dataFiles.append(dataUtils.getDataFileNameOnly(df))        
        self.cleanRegex = re.compile('[\!\*\?]+')
        self.pprintr = pprint.PrettyPrinter(indent=4) 
      
    def storeNodes(self, dataReader, dataFile):        
        transaction = self.graphdb.transaction() 
        print 'Creating indexes for ' + dataFile      
        index = self.getIndex(dataFile)
        count = 0
        fieldsDict = {}
        firstRow = True 
        try:       
            for row in dataReader:
                if (firstRow == True):
                    fields = row    
                    for r in row : 
                        fieldsDict.__setitem__(r,r)                                          
                    firstRow = False
                else:
                    data = {'dataFile':dataFile}               
                    i = 0
                    for f in fields:                                       
                        data.__setitem__(f, unicode(row[i], 'utf-8'))                        
                        i = i + 1                        
                    n = self.graphdb.node(**data)
                    count = count + 1         
                    for f in fields:                    
                        index.add(data[f], n)                                          
          
            fieldsDict.__setitem__('dataFile','dataFile')
            n = self.graphdb.node(**fieldsDict)          
            index.add("dataTypeProps", n)                          
            
            transaction.success()   
            print 'Total ' + str(count) + ' items'
        finally: 
            transaction.finish()
    
    def storeRelations(self):
        print 'Updating relations...'
        i = 0
        relationsCount = 0
        n = []
        transaction = self.graphdb.transaction()
        grm = data.gamesRelationsMapper._gamesRelationsMapper() 
        try:
            indexes = self.getAllIndexes()
            while (n != None):
                try: 
                    n = self.graphdb.node[i]
                    i = i + 1                    
                except: n = None
                
                if n == None or not n.__contains__('dataFile') or not indexes.__contains__(n['dataFile']): 
                    continue
                
                dataTypeProps = indexes[n['dataFile']].match("dataTypeProps")   
                for dataTypeProp in dataTypeProps:
                    for dtp in dataTypeProp:                      
                        if len(n[dtp])>0 and grm.relations.__contains__(n['dataFile']) and grm.relations[n['dataFile']].__contains__(dtp):                            
                            parts = [n[dtp]]                           
                            if ',' in n[dtp]: parts = n[dtp].split(',')  #Multiple values detected
                                
                            for part in parts:
                                others = indexes[grm.relations[n['dataFile']][dtp]].match(self.cleanStr(part))
                                if (others.__len__() <=0 ) : continue 
                                for other in others:
                                    if n == other : continue
                                    #self.pprintr.pprint(n['name'] +' <- ' + part + ' -> '+ other['name'])  
                                    n.RELATED_TO(other,**{'type':dtp})   
                                    relationsCount = relationsCount + 1                       
                    break              
                if (i % 500) == 0 : print str(i) + ' items processed'
                
            print str(i) + ' items processed'
            print 'Total relations created ' + str(relationsCount)
            transaction.success()      
        finally: 
            transaction.finish()
            
    def getNode(self, dataFile, q):
        transaction = self.graphdb.transaction() 
        try:               
            indexes = self.getAllIndexes()
            transaction.success()       
                   
            dataTypeProps = indexes[dataFile].match("dataTypeProps")         
            hits = indexes[dataFile].match(self.cleanStr(q))          
                     
            if hits == None or hits.__len__() == 0 or dataTypeProps == None or dataTypeProps.__len__() == 0:
                return None
           
            results = []
            for dtProps in dataTypeProps:
                for hit in hits:   
                    item = {}
                    for dtp in dtProps:                     
                        item.__setitem__(dtp, hit[dtp])                        
                      
                    relatedItems = []
                    for related in data.defaultTraverse._defaultTraverse(hit):
                        #rid={}
                        #relateddtProps = indexes[related['dataFile']].match("dataTypeProps") 
                        #for rdp in relateddtProps:
                        #    for rdpp in rdp:                     
                        #        rid.__setitem__(rdpp, related[rdpp])
                        #    break
                        rid = {'dataFile':related['dataFile'], 'name':related['name'], 'id':related['id']}
                        relatedItems.append(rid)
                      
                    item.__setitem__('related', relatedItems)
                    results.append(item)
                break            
                         
            return results        
        finally:
            transaction.finish() 
            
    def cleanUp(self):
        self.graphdb.shutdown()
    
    def getIndex(self, dataFile):
        return self.graphdb.index(dataUtils.getDataFileNameOnly(dataFile), create=True, full_text='full_text')
    
    def getAllIndexes(self):
        indexes = {}
        for df in self.dataFiles:               
            indexes.__setitem__(df, self.getIndex(df))
        return indexes
    
    def cleanStr(self, value):
        return self.cleanRegex.sub(r'', value)
            