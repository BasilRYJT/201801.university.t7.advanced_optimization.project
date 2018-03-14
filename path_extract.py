"""
Python Script to visualise solutions as paths on a map.
"""
def parseAPI(params):
    import requests
    import polyline
    print(">>> Parser BEGIN")
    print(">>> Request BEGIN")
    r = requests.get("https://maps.googleapis.com/maps/api/directions/json",params=params)
    if r.status_code != 200:
        print(params)
        raise PermissionError(" Request FAILURE. status code: %s; %s" %(r.status_code,params))
    else:
        print(">>> Request SUCCESS")
        try:
            raw = r.json()["routes"][0]["overview_polyline"]["points"]
            coordList = polyline.decode(raw)
            n=1
            with open("./output/map_data_2.csv", "a") as out_file:
                for i in coordList:
                    out_file.write("%s,%s,%s\n" %(i[0],i[1],n))
                    n+=1
        except IndexError:
            print(r.json())
            raise PermissionError("OVER_QUERY_LIMIT")
        print(">>> Parser END")

def getPath(filename,tokenKey):
    import pandas as pd
    from keyGen.token import getToken
    dataset = pd.read_csv("./output/%s" % filename, dtype="str")
    apiKey = getToken(tokenKey)
    print("########## START SCRIPT ##########")
    params = {
            "origin":"",
            "destination":"",
            "key":apiKey,
            "mode":"transit",
            }
    for i in range(dataset.shape[0]):
        params["origin"] = "%s,%s" %(dataset["ori_lat"][i],dataset["ori_lon"][i])
        params["destination"] = "%s,%s" %(dataset["des_lat"][i],dataset["des_lon"][i])
        parseAPI(params)        
    print("########## END SCRIPT ##########")

getPath("20180220_noon_solution_seq.csv", "Jkdso71YjuVV9ZN")