import json
import datetime

# jam level mapping:
# level 0: Free flow
# level 1: Light traffic
# level 2: Moderate traffic
# level 3: Heavy traffic
# level 4: Bumper to bumper

def MperS2MiperH(inputMperS):
    return inputMperS * 2.23694


def CSVFilesGenerator(inputDT, inputStr, targetDir):
    # get current time stamp
    CurTimeStr = inputDT.strftime('%Y-%m-%d %H:%M:%S')
    FileName = inputDT.strftime('%Y%m%d%H%M')

    RealJson = json.loads(inputStr)

    SRHeader = ['Route Name', 'Time Stamp', 'From Street', 'To Street', 'Length (meters)', 'Historical Travel Time (seconds)', 'Travel Time (seconds)', 'Historical Speed (mph)', 'Speed (mph)', 'Jam Level']
    with open(targetDir + '\\' + 'SR_' + FileName + '.csv', 'a') as outputSubroutesFile:
        outputSubroutesFile.write(','.join(SRHeader) + '\n')

    ALHeader = ['Id', 'Report Time', 'Reported By', 'Alert Type', 'SubType', 'Street Name', 'City', 'Latitude', 'Longitude']
    with open(targetDir + '\\' + 'AL_' + FileName + '.csv', 'a') as outputAlertroutesFile:
        outputAlertroutesFile.write(','.join(ALHeader) + '\n')

    RTHeader = ['Route Name', 'Time Stamp', 'Id', 'Length (meters)', 'Historical Travel Time (seconds)', 'Travel Time (seconds)', 'Historical Speed (mph)', 'Speed (mph)', 'Jam Level']
    with open(targetDir + '\\' + 'RT_' + FileName + '.csv', 'a') as outputRoutesFile:
        outputRoutesFile.write(','.join(RTHeader) + '\n')

    for route in RealJson['routes']:
        outputList = []
        outputList.append(route['name'].lower())
        outputList.append(CurTimeStr)
        outputList.append(str(route['id']))
        outputList.append(str(route['length']))
        outputList.append(str(route['historicTime']))
        outputList.append(str(route['time']))
        outputList.append(str(MperS2MiperH(route['length'] / route['historicTime'])))
        outputList.append(str(MperS2MiperH(route['length'] / route['time'])))
        outputList.append(str(route['jamLevel']))
        try:
            for subroute in route['subRoutes']:
                subRouteList = []
                subRouteList.append(route['name'].lower())
                subRouteList.append(CurTimeStr)
                subRouteList.append(subroute['fromName'].lower())
                subRouteList.append(subroute['toName'].lower())
                subRouteList.append(str(subroute['length']))
                subRouteList.append(str(subroute['historicTime']))
                subRouteList.append(str(subroute['time']))
                subRouteList.append(str(MperS2MiperH(subroute['length'] / subroute['historicTime'])))
                subRouteList.append(str(MperS2MiperH(subroute['length'] / subroute['time'])))
                subRouteList.append(str(subroute['jamLevel']))
                with open(targetDir + '\\' + 'SR_' + FileName + '.csv', 'a') as outputSubroutesFile:
                    outputSubroutesFile.write(','.join(subRouteList) + '\n')

                if 'leadAlert' in subroute:
                    AlertList = []
                    AlertList.append(subroute['leadAlert']['id'])
                    AlertList.append(datetime.datetime.fromtimestamp(int(subroute['leadAlert']['reportTime'] / 1000)).strftime('%Y-%m-%d %H:%M:%S'))
                    AlertList.append(subroute['leadAlert']['reportByNickname'])
                    AlertList.append(subroute['leadAlert']['type'])
                    AlertList.append(subroute['leadAlert']['subType'])
                    AlertList.append(subroute['leadAlert']['street'].lower())
                    AlertList.append(subroute['leadAlert']['city'].lower().replace(',', ' '))
                    AlertList.append(subroute['leadAlert']['position'].split(' ')[0])
                    AlertList.append(subroute['leadAlert']['position'].split(' ')[1])

                    with open(targetDir + '\\' + 'AL_' + FileName + '.csv', 'a') as outputAlertroutesFile:
                        outputAlertroutesFile.write(','.join(AlertList) + '\n')

            with open(targetDir + '\\' + 'RT_' + FileName + '.csv', 'a') as outputRoutesFile:
                outputRoutesFile.write(','.join(outputList) + '\n')
        except KeyError, e:
            print e.message + ' === ' + route['name'].lower() + ' -- ' + str(route['id'])