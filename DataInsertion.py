__author__ = 'Kaiqun'

from DBConnector import DatabaseConnection
import json

def insertor(inputDT, inputStr):
    CurTime = inputDT.strftime('%Y-%m-%d')

    db = DatabaseConnection('WazeScrapping')

    dataCollection = db[CurTime]

    RealJson = json.loads(inputStr)

    RealJson.update({'DateTime': inputDT})

    dataCollection.insert(RealJson)