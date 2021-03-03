import os
import xml.etree.ElementTree as ET
import datetime
import pandas as pd
global n_file
global n_parse
global n_record
global n_error

def convert_time(time_str):
    if "上午" in time_str:
        date=datetime.datetime.strptime(time_str, " %Y/%m/%d 上午 %H:%M:%S")
        return date
    if "下午" in time_str:
        time_str.replace(" 下午 ", " ")
        date=datetime.datetime.strptime(time_str," %Y/%m/%d 下午 %H:%M:%S")
        if date.hour==12:
            return date
        else:
            return (date+datetime.timedelta(hours=12))

def append_df(xml_file,df):
    print("parsing %s" % n_file)
    global n_parse
    global n_record
    global n_error
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for child in root:
            dict={}
            text = ""
            for child in child:
                if child.tag == "{http://data.one.gov.hk/td}%s"%"ReferenceDate" and child.text != None:
                    date=convert_time(child.text)
                    dict["Date"]=date
                if child.tag == "{http://data.one.gov.hk/td}%s" % "EngText" and child.text != None:
                    text = child.text.lower()
                    dict["Text"]=text.replace("\n"," ")
            if len(text) != 0:
                n_record = n_record + 1
                df=df.append(dict,ignore_index=True)
        n_parse = n_parse + 1
    except:
        n_error = n_error + 1
    return df


if __name__ == '__main__':
    file_path1 = './original dataset/2016020191004(1st generation)'
    df1=pd.DataFrame(columns=["Date","Text"])
    n_file=0
    n_parse=0
    n_record=0
    n_error=0
    for fpath, dirname, allfname in os.walk(file_path1):
        for fname in allfname:
            if fname.endswith('.xml'):
                n_file=n_file+1
                xml_path = os.path.join(fpath, fname)
                df1=append_df(xml_path,df1)
                # append_json(xml_path,save_path1)
    print("file number: %s"%n_file)
    print("parse number: %s" % n_parse)
    print("record number: %s" % n_record)
    print("error number: %s" % n_error)
    df1.to_csv("df_1st.csv",index=False)

