import pandas as pd
import numpy as np
import json
df1=pd.read_csv("df_2nd.csv", header=0,index_col=False,parse_dates=["Date"])
print(df1.shape[0])
df_drop=df1.drop_duplicates(subset=["Text"],keep="first")
print(df_drop.shape[0])
cols=["Incident_cause","Status","Location",
                                "Direction_landmark","Near_landmark","Between_landmark"]
df_drop=df_drop.reset_index(drop=True)
df_drop.to_csv("tn_2nd_dump.csv",index=True)
label=0
with open("tn_2nd_dump.json", "a")as f:
    for index, row in df_drop.iterrows():
        label_list = []
        for col in cols:
            if row[col]is not np.nan:
                label_list.append({col: row[col]})
                label=label+1
        # jsonData = json.dumps(
        #             {'index': index, 'text': row["Text"], 'label_list': label_list}, indent=4)
        if row["Date"] is not pd.NaT:
            jsonData = json.dumps({'index': index,'text': row["Text"],'date': str(row["Date"]), 'label_list': label_list}, indent=4)
            f.write(jsonData + "\n")
        if row["Date"] is pd.NaT:
            jsonData = json.dumps({'index': index, 'text': row["Text"], 'label_list': label_list},
                                  indent=4)
            f.write(jsonData + "\n")
print(label)

