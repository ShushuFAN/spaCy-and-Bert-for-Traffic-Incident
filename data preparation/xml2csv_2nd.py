import os
import xml.etree.ElementTree as ET
import pandas as pd
global n_file
global n_parse
global n_record
global n_error

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
                if child.tag == "INCIDENT_DETAIL_EN" or child.tag == "INCIDENT_SUBTYPE_EN" and child.text != None:
                    cause = child.text.lower()
                    dict["Incident_cause"] = cause
                if child.tag == "ANNOUNCEMENT_DATE" and child.text != None:
                    date = child.text.lower()
                    date.replace("T", " ")
                    dict["Date"]=date
                if child.tag == "LOCATION_EN" and child.text != None:
                    location = child.text.lower()
                    dict["Location"] = location
                if child.tag == "DIRECTION_EN" and child.text != None:
                    direction = child.text.lower()
                    dict["Direction_landmark"] = direction
                if child.tag == "INCIDENT_STATUS_EN" and child.text != None:
                    status = child.text.lower()
                    dict["Status"] = status
                if child.tag == "NEAR_LANDMARK_EN" and child.text != None:
                    near_landmark = child.text.lower()
                    dict["Near_landmark"] = near_landmark
                if child.tag == "BETWEEN_LANDMARK_EN" and child.text != None:
                    between_landmark = child.text.lower()
                    dict["Between_landmark"] = between_landmark
                if child.tag == "CONTENT_EN" and child.text != None:
                    text = child.text.lower()
                    dict["Text"] = text.replace("\n", " ")
            if len(text) != 0:
                n_record = n_record + 1
                df=df.append(dict,ignore_index=True)
        n_parse = n_parse + 1
    except:
        n_error = n_error + 1
    return df



if __name__ == '__main__':
    file_path2 = './original dataset/20191005-2020(2nd generation)'
    df1 = pd.DataFrame(columns=["Date", "Text","Incident_cause","Location",
                                "Direction_landmark","Status","Near_landmark","Between_landmark"])
    n_file=0
    n_parse=0
    n_record=0
    n_error=0
    for fpath, dirname, allfname in os.walk(file_path2):
        for fname in allfname:
            if fname.endswith('.xml'):
                n_file=n_file+1
                xml_path = os.path.join(fpath, fname)
                df1=append_df(xml_path,df1)
    print("file number: %s"%n_file)
    print("parse number: %s" % n_parse)
    print("record number: %s" % n_record)
    print("error number: %s" % n_error)
    df1.to_csv("df_2nd.csv",index=False)
    print(df1.shape[0])