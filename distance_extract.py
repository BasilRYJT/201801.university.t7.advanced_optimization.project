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
    percentage = round(pos/total, 2)
    return "[ "+str(percentage)+"% ]"

def getUNIXTime(h,m=0):
    from datetime import datetime
    from time import mktime
    raw = datetime(2018,2,20,h,m,0)
    return mktime(raw.timetuple())

def parseAPI(params,dataset,i,j):
    import requests
    from copy import deepcopy
    print(">>> Parser BEGIN")
    print(">>> Request BEGIN")
    r = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json",params=params)
    if r.status_code != 200:
        print(params)
        raise Exception(" Request FAILURE. status code: "+str(r.status_code)+" ; location: "+str(i)+","+str(j))
    else:
        print(">>> Request SUCCESS")
        try:
            data = r.json()["rows"][0]["elements"]
            ori = str(dataset["name"][i])
            for k in range(len(data)):
                if data[k]["status"] == "OK":
                    output = deepcopy(ori)
                    output += ","+str(dataset["name"][j-len(data)+k])
                    output += ","+str(data[k]["distance"]["text"])
                    output += ","+str(data[k]["distance"]["value"])
                    output += ","+str(data[k]["duration"]["text"])
                    output += ","+str(data[k]["duration"]["value"])        
                    with open("./output/20180220_noon.csv","a") as out_file:
                        out_file.write(output+"\n")
                    print(getProgress(i,j,dataset.shape[0])+" "+output)
                else:
                    with open("./output/20180220_faillog.csv","a") as out_file:
                        out_file.write(ori+","+str(dataset["name"][j])+","+str(i)+","+str(j))
                    print(getProgress(i,j,dataset.shape[0])+" FAILED: "+ori+","+str(dataset["name"][j])+","+str(i)+","+str(j))
        except IndexError:
            raise PermissionError("OVER_QUERY_LIMIT")
        print(">>> Parser END")
            

def main(ori=0,des=0):
    import pandas as pd
    from keyGen.token import getToken
    dataset = pd.read_csv("./data/hawker_location.csv", dtype="str")
    apiKey = getToken("Te76tgkVJftylWM")
    deptime = str(int(getUNIXTime(12)))
    params = {
            "origins":"",
            "destinations":"",
            "key":apiKey,
            "mode":"transit",
            "departure_time":deptime
            }
    print("########## START SCRIPT ##########")
    for i in range(ori,dataset.shape[0]):
        params["origins"] = dataset["lat"][i]+","+dataset["lon"][i]
        eleCount = 0
        destEle = ""
        for j in range(des,dataset.shape[0]):
            if i != j:
                eleCount += 1
                destEle += dataset["lat"][j]+","+dataset["lon"][j]+"|"
                if eleCount >= 25:
                    destEle = destEle[:-1]
                    params["destinations"] = destEle
                    parseAPI(params,dataset,i,j)
                    eleCount = 0
                    destEle = ""
        if eleCount > 0:
            destEle = destEle[:-1]
            params["destinations"] = destEle
            parseAPI(params,dataset,i,j)
    print("########## END SCRIPT ##########")
                                         
main()