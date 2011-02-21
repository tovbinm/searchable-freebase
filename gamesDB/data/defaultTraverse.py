'''
Created on Feb 21, 2011

@author: matthew
'''
import neo4j

class _defaultTraverse(neo4j.Traversal):
    types = [neo4j.Undirected.RELATED_TO]
    
    order = neo4j.BREADTH_FIRST
    stop = neo4j.StopAtDepth(1)
    returnable = neo4j.RETURN_ALL_BUT_START_NODE
