"""
Python script that checks connectivity of resulting dataset from queries
"""

def checkFile(filename):
    import pandas as pd
    print("########## START SCRIPT ##########")
    dataset = pd.read_csv("./output/"+filename)
    print(">>> Import SUCCESS")
    locList = dataset["ori"].unique().tolist()
    count = 0
    with open("./output/"+filename[:-4]+"_errors.csv","a") as out_file:
        print(">>> Check BEGIN")
        for ori in locList:
            subset = dataset.loc[dataset["ori"]==ori,:]
            for des in locList:
                if ori != des:
                    if subset.loc[subset["des"]==des,:].empty:
                        count += 1
                        out_file.write(ori+","+des+","+str(locList.index(ori))+","+str(locList.index(des))+"\n")
                        print("ERROR FOUND: Mising Pair "+ori+" - "+des)
                    if subset.loc[subset["des"]==des,:].shape[0] > 1:
                        count += 1
                        print("ERROR FOUND: Duplicate Pair "+ori+" - "+des)
                        for i in range(subset.loc[subset["des"]==des,:].shape[0]):
                            out_file.write(ori+","+des+","+str(locList.index(ori))+","+str(locList.index(des))+"\n")
                else:
                    if not subset.loc[subset["des"]==des,:].empty:
                        count += 1
                        out_file.write(ori+","+des+","+str(locList.index(ori))+","+str(locList.index(des))+"\n")
                        print("ERROR FOUND: Self-Assignment "+ori)
    print(">>> Check END")
    print("Number of Errors found: "+str(count))
    print("########## END SCRIPT ##########")

checkFile("20180220_noon.csv")               
            