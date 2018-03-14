"""
Python script for the procedural extraction of distances between hawker centres
in Singapore.
"""

def fac(n):
    if n == 0:
        return 1
    else:
        return n*fac(n-1)

def getProgress(i, j, n):
    if i > j:
        pos = i*(n-1) + j
    else:
        pos = i*(n-1) + j - 1
    total = float(fac(n)/fac(n-2))
    percentage = round(100*pos/total, 2)
    return "[ "+str(percentage)+"% ]"

def getUNIXTime(hm):
    from datetime import datetime
    from time import mktime
    raw = datetime(2018,3,8,hm[0],hm[1],0)
    return mktime(raw.timetuple())

def parseAPI(params,dataset,i,j,time=None):
    import requests
    from copy import deepcopy
    print(">>> Parser BEGIN")
    print(">>> Request BEGIN")
    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json",params=params)
    if r.status_code != 200:
        print(params)
        raise PermissionError(" Request FAILURE. status code: "+str(r.status_code)+" ; location: "+str(i)+","+str(j))
    else:
        print(">>> Request SUCCESS")
        try:
            data = r.json()["rows"][0]["elements"]
            ori = str(dataset["name"][i])
            for k in range(len(data)):
                if data[k]["status"] == "OK":
                    output = deepcopy(ori)
                    if (j-len(data)+k) < i:
                        output += ","+str(dataset["name"][j-len(data)+k])
                    else:
                        output += ","+str(dataset["name"][j+1-len(data)+k])
                    output += ","+str(data[k]["distance"]["text"])
                    output += ","+str(data[k]["distance"]["value"])
                    output += ","+str(data[k]["duration"]["text"])
                    output += ","+str(data[k]["duration"]["value"])
                    if time:
                        output += ",%s:%s"%time
                    with open("./output/20180308_time.12.csv","a") as out_file:
                        out_file.write(output+"\n")
                    print(getProgress(i,j,dataset.shape[0])+" "+output)
                else:
                    with open("./output/20180308_faillog.12.csv","a") as out_file:
                        out_file.write(ori+","+str(dataset["name"][j])+","+str(i)+","+str(j))
                    print(getProgress(i,j,dataset.shape[0])+" FAILED: "+ori+","+str(dataset["name"][j])+","+str(i)+","+str(j))
        except IndexError:
            print(r.json())
            raise PermissionError("OVER_QUERY_LIMIT")
        print(">>> Parser END")

def correctErrors(filename,tokenKey):
    import pandas as pd
    from keyGen.token import getToken
    dataset = pd.read_csv("./data/hawker_location.csv", dtype="str")
    error = pd.read_csv("./output/%s"%filename)
    apiKey = getToken(tokenKey)
    deptime = str(int(getUNIXTime(12)))
    params = {
            "origins":"",
            "destinations":"",
            "key":apiKey,
            "mode":"transit",
            "departure_time":deptime
            }
    print("########## START SCRIPT ##########")
    ithList = error["ith"].tolist()
    jthList = error["jth"].tolist()
    for i in range(error.shape[0]):
        params["origins"] = dataset["lat"][ithList[i]]+","+dataset["lon"][ithList[i]]
        params["destinations"] = dataset["lat"][jthList[i]]+","+dataset["lon"][jthList[i]]
        parseAPI(params,dataset,ithList[i],jthList[i])
    print("########## END SCRIPT ##########")
          
def main(filename,tokenKey,timeList=[(12,0)],ori=0,des=0):
    import pandas as pd
    from keyGen.token import getToken
    dataset = pd.read_csv("./data/%s" % filename, dtype="str")
    apiKey = getToken(tokenKey)
    print("########## START SCRIPT ##########")
    for time in timeList:
        deptime = str(int(getUNIXTime(time)))
        print(">>> Get TIME: %s:%s" % time)
        params = {
                "origins":"",
                "destinations":"",
                "key":apiKey,
                "mode":"transit",
                "departure_time":deptime
                }
        for i in range(ori,dataset.shape[0]):
            params["origins"] = dataset["lat"][i]+","+dataset["lon"][i]
            eleCount = 0
            destEle = ""
            if i == ori:
                start = des
            else:
                start = 0
            for j in range(start,dataset.shape[0]):
                if i != j:
                    eleCount += 1
                    destEle += dataset["lat"][j]+","+dataset["lon"][j]+"|"
                    if eleCount >= 25:
                        destEle = destEle[:-1]
                        params["destinations"] = destEle
                        parseAPI(params,dataset,i,j,time)
                        eleCount = 0
                        destEle = ""
            if eleCount > 0:
                destEle = destEle[:-1]
                params["destinations"] = destEle
                parseAPI(params,dataset,i,dataset.shape[0]-1,time)
    print("########## END SCRIPT ##########")
          
def getTimeList(start, end, inter=30):
    timeList = []
    hr = start[0]
    mn = start[1]
    timeList.append((hr, mn))
    duration = (end[0]*60+end[1]) - (start[0]*60+start[1])
    if duration < 0:
        raise ValueError("Start Time is later than End Time.")
    for i in range(duration//inter):
        mn += inter
        if mn >= 60:
            mn -= 60
            hr += 1
        timeList.append((hr, mn))
    if duration%inter:
        mn += duration%inter
        if mn >= 60:
            mn -= 60
            hr += 1
        timeList.append((hr, mn))
    return timeList

timeList = getTimeList((17,0),(21,0))
main("hawker_location.act5.csv","ek8cyqTVUfHzwdA",timeList=timeList)
