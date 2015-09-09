__author__ = 'Kaiqun'

import pymongo

mongodb_uri = 'mongodb://10.41.20.61:12345'

def DatabaseConnection(targetDB):
    try:
        connection = pymongo.Connection(mongodb_uri)
        return connection[targetDB]
    except:
        print('Error: Unable to connect to database.')
        return None