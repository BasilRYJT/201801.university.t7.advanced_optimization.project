"""
Python Script to decode hash key used in dat files.
"""

def translatePair(filename, dictionary,coord=None):
    import pandas as pd
    print("########## START SCRIPT ##########")
    dataset = pd.read_csv("./output/%s" % filename, dtype="str")
    nameDict = pd.read_csv("./output/%s" % dictionary, dtype="str")
    if coord:
        coordFile = pd.read_csv("./data/%s" % coord, dtype="str")
    print(">>> Import SUCCESS")
    with open("./output/%s_seq.csv"%filename[:-4],"a") as out_file:
        for i in range(dataset.shape[0]):
            oriHash = dataset["ori"][i]
            desHash = dataset["des"][i]
            ind = i+1
            ori = nameDict[nameDict.key == oriHash]["value"].tolist()[0]
            des = nameDict[nameDict.key == desHash]["value"].tolist()[0]
            if coord:
                oriLat = coordFile[coordFile.name == ori]["lat"].tolist()[0]
                oriLon = coordFile[coordFile.name == ori]["lon"].tolist()[0]
                desLat = coordFile[coordFile.name == des]["lat"].tolist()[0]
                desLon = coordFile[coordFile.name == des]["lon"].tolist()[0]
            else:
                oriLat = nameDict[nameDict.key == oriHash]["lat"].tolist()[0]
                oriLon = nameDict[nameDict.key == oriHash]["lon"].tolist()[0]
                desLat = nameDict[nameDict.key == desHash]["lat"].tolist()[0]
                desLon = nameDict[nameDict.key == desHash]["lon"].tolist()[0]
            row = "%s,%s,%s,%s,%s,%s,%s\n" %(ind,ori,des,oriLat,oriLon,desLat,desLon)
            print(row)
            out_file.write(row)
    print("########## END SCRIPT ##########")

translatePair("20180220_noon_solution.csv","20180220_noon_dict.csv","hawker_location.csv")
