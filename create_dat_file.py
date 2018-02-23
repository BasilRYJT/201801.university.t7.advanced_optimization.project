"""
Python script for the conversion of csv files into ampl readible dat files.
"""

def convertCSV(filename):
    import pandas as pd
    import hashlib
    import base64
    print("########## START SCRIPT ##########")
    dataset = pd.read_csv("./output/"+filename)
    print(">>> Import SUCCESS")
    locList = dataset["ori"].unique().tolist()
    indList = [base64.urlsafe_b64encode(hashlib.md5(loc.encode("utf-8")).digest()).decode("utf-8").replace("=","A").replace("-","B") for loc in locList]
    indDict = {base64.urlsafe_b64encode(hashlib.md5(loc.encode("utf-8")).digest()).decode("utf-8").replace("=","A").replace("-","B"):loc for loc in locList}
    print(indList)
    with open("./output/%sdat"%filename[:-3],"a") as out_file:
        print(">>> Parser BEGIN")
        out_file.write("data;\n\nset VER := ")
        for loc in indList:
            out_file.write(loc + " ")
        print(">>> Vertices COMPLETE")
        out_file.write(";\n\nset EDG :=\n")
        for ori in indList:
            out_file.write("(%s,*) "%ori)
            for des in indList:
                if ori != des:
                    out_file.write(des+" ")
            out_file.write("\n")
        print(">>> Edges COMPLETE")
        out_file.write(";\n\nparam weight :=\n")
        for ori in indList:
            out_file.write("[%s,*] "%ori)
            for des in indList:
                if ori != des:
                    val = dataset[dataset["ori"]==indDict[ori]].loc[dataset["des"]==indDict[des],"time_val"].tolist()[0]
                    out_file.write("%s %s "%(des,val))
            out_file.write("\n")
        out_file.write(";")
        print(">>> Weights COMPLETE")
        print(">>> Parser END")
        with open("./output/%s_dict.csv"%filename[:-4],"a") as out_file:
            print(">>> Dict Write BEGIN")
            out_file.write("key,value\n")
            for loc in indList:
                out_file.write("%s,%s\n"%(loc,indDict[loc]))
            print(">>> Dict Write END")
        print("########## END SCRIPT ##########")

convertCSV("20180220_noon_18.csv")
convertCSV("20180220_noon.csv")        
            
        
    