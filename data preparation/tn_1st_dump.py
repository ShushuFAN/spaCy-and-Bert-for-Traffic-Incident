import pandas as pd
df1=pd.read_csv("df_1st.csv", header=0,index_col=False,parse_dates=["Date"])
print(df1.shape[0])
df_drop=df1.drop_duplicates(subset=["Text"],keep="first")
df_drop=df_drop.reset_index(drop=True)
df_drop.to_csv("tn_1st_dump.csv",index=True)
print(df_drop.shape[0])