__author__ = 'Kaiqun'

from requests.auth import HTTPBasicAuth
import requests
import re
import time
import datetime
from DataInsertion import insertor
from CSVFileGen import CSVFilesGenerator


if __name__ == '__main__':
    while True:
        with open('credentials', 'r') as crdts:
            oneline = crdts.readline()
            link = oneline.split(',')[0]
            user = oneline.split(',')[1]
            pwd = oneline.split(',')[2]
            FileLocation = oneline.split(',')[3]

        r = requests.get(link, auth=HTTPBasicAuth(user, pwd))

        # remove Lines
        jsonTextNoLines = re.sub(r'("Line":\[|)\{"x":-\d+.\d+,"y":\d+.\d+\}(,|)(\],|)', '', r.text, flags=re.IGNORECASE)

        # remove bboxes
        jsonTextNoLines = re.sub(r'"bbox":\{"minY":\d+.\d+,"minX":-\d+.\d+,"maxY":\d+.\d+,"maxX":-\d+.\d+\}(,|)', '',
                                 jsonTextNoLines, flags=re.IGNORECASE)

        # get current time stamp
        CurTime = datetime.datetime.now()
        CurTimeStr = CurTime.strftime('%Y-%m-%d %H:%M:%S')

        insertor(CurTime, jsonTextNoLines)

        CSVFilesGenerator(CurTime, jsonTextNoLines, FileLocation)

        print CurTimeStr + ' Data Operated. '

        time.sleep(3 * 60)