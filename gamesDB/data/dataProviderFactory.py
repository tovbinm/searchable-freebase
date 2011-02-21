'''
Created on Feb 19, 2011

@author: matthew
'''

import data.providers.neo4jdataProvider

class _dataProviderFactory(object):
    def getDataProvider(self,dataProvidername,dataProviderParams):
        
        if dataProvidername.lower() == 'neo4j':
            return data.providers.neo4jdataProvider.neo4jdataProvider(dataProviderParams);
        
        raise Exception('"'+dataProvidername+'"' + 'was not found')