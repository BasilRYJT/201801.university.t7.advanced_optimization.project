"""
Python script for the conversion of csv files into ampl readible dat files.
"""

def convertCSV(filename):
    import pandas as pd
    dataset = pd.read_csv("./output/"+filename)
    locList = list(set(dataset["ori"]))
    with open("./output/"+filename[:-3]+"dat","a") as out_file:
        out_file.write("data;\n\nset ORIG := ")
        for loc in range(len(locList)):
            out_file.write()
            
            
        
    