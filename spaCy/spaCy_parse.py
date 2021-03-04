import pandas as pd
import spacy
from spacy.matcher import Matcher
import re
import json
model_dir = "./models/model_up"
nlp = spacy.load(model_dir)
matcher = Matcher(nlp.vocab)
pattern1 = [{"POS":"ADJ"},{"LEMMA": "lane"}, {"LOWER": "of"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "bound"}, {"LOWER": "near"}, {"ENT_TYPE": "FAC", "OP": "*"}]
pattern1_1 = [{"POS":"DET"},{"LEMMA": "lane"}, {"LOWER": "of"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "bound"}, {"LOWER": "near"}, {"ENT_TYPE": "FAC", "OP": "*"}]
pattern2 = [{"POS":"ADJ"},{"LEMMA": "lane"}, {"LOWER": "of"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "bound"}, {"LOWER": "between"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "and"}, {"ENT_TYPE": "FAC", "OP": "*"}]
pattern2_2 = [{"POS":"DET"},{"LEMMA": "lane"}, {"LOWER": "of"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "bound"}, {"LOWER": "between"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "and"}, {"ENT_TYPE": "FAC", "OP": "*"}]
pattern3 = [{"POS":"ADJ"},{"LEMMA": "lane"}, {"LOWER": "of"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "both"}, {"LEMMA": "bound"}, {"LOWER": "near"}, {"ENT_TYPE": "FAC", "OP": "*"}]
pattern3_2 = [{"POS":"DET"},{"LEMMA": "lane"}, {"LOWER": "of"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "both"}, {"LEMMA": "bound"}, {"LOWER": "near"}, {"ENT_TYPE": "FAC", "OP": "*"}]
pattern4 = [{"POS":"ADJ"},{"LEMMA": "lane"}, {"LOWER": "of"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "both"}, {"LEMMA": "bound"}, {"LOWER": "between"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "and"}, {"ENT_TYPE": "FAC", "OP": "*"}]
pattern4_2 = [{"POS":"DET"},{"LEMMA": "lane"}, {"LOWER": "of"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "both"}, {"LEMMA": "bound"}, {"LOWER": "between"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "and"}, {"ENT_TYPE": "FAC", "OP": "*"}]
pattern5 = [{"LOWER": "at"}, {"ENT_TYPE": "FAC", "OP": "*"}, {"LOWER": "near"}, {"ENT_TYPE": "FAC", "OP": "*"}]
pattern6 = [{"LOWER": "bound", "OP": "!"}, {"LOWER": "between"}, {"ENT_TYPE": "FAC", "OP": "*"},
            {"LOWER": "and"}, {"ENT_TYPE": "FAC", "OP": "*"}]
matcher.add("LANE_NEAR_ALL", None, pattern1)
matcher.add("LANE_NEAR_ALL", None, pattern1_1)
matcher.add("LANE_BETWEEN_ALL", None, pattern2)
matcher.add("LANE_BETWEEN_ALL", None, pattern2_2)
matcher.add("LANE_NEAR_BOTH", None, pattern3)
matcher.add("LANE_NEAR_BOTH", None, pattern3_2)
matcher.add("LANE_BETWEEN_BOTH", None, pattern4)
matcher.add("LANE_BETWEEN_BOTH", None, pattern4_2)
matcher.add("LOCATION_NEAR", None, pattern5)
matcher.add("BETWEEN_AND", None, pattern6)

cols=["Incident_cause","Location",
                                "Direction_landmark","Status","Near_landmark","Between_landmark"]

def match_labels(string_id, span,label_list):
    list_ents = span.ents
    if string_id == "LANE_NEAR_ALL":
        label_list.extend([{"Lane_landmark": span[0].text},{"Location":list_ents[0].text},
                          {"Direction_landmark":list_ents[1].text},{"Near_landmark":list_ents[2].text}])
        return label_list

    elif string_id == "LANE_NEAR_BOTH":
        label_list.extend([{"Lane_landmark": span[0].text},{"Location":list_ents[0].text},
                          {"Direction_landmark":"both"},{"Near_landmark":list_ents[1].text}])
        return label_list

    elif string_id == "LANE_BETWEEN_ALL":
        label_list.extend([{"Lane_landmark": span[0].text},{"Location":list_ents[0].text},
                          {"Direction_landmark":list_ents[1].text},{"Near_landmark":list_ents[2].text},
                          {"Between_landmark":list_ents[3].text}])
        return label_list

    elif string_id == "LANE_BETWEEN_BOTH":
        label_list.extend([{"Lane_landmark": span[0].text},{"Location":list_ents[0].text},
                          {"Direction_landmark":"both"},{"Near_landmark":list_ents[1].text},
                          {"Between_landmark":list_ents[2].text}])
        return label_list

    elif string_id == "LOCATION_NEAR":
        label_list.extend([{"Location":list_ents[0].text},
                          {"Near_landmark":list_ents[1].text}])
        return label_list

    elif string_id == "BETWEEN_AND":
        label_list.extend([{"Near_landmark":list_ents[0].text},
                          {"Between_landmark":list_ents[1].text}])
        return label_list
def location(doc):
    label_list=[]
    index = -1
    for token in doc:
        index=index+1
        if token.text in ["lane","lanes","lane(s)","lane(s","lane("]:
            span=doc[index:-1]
            # print(span.text)
            for ent in span.ents:
                if ent.label_=="FAC":
                    label_list.append({"Location": ent.text})
                    break
            break
    # print(label_list)
    return label_list
def direction(doc):
    label_list=[]
    index = -1
    for token in doc:
        index=index+1
        if token.text == "bound":
            span=doc[0:index]
            # print(span.text)
            FACs=[]
            for ent in span.ents:
                if ent.label_=="FAC":
                    FACs.append(ent.text)
            label_list.append({"Direction_landmark": FACs[-1]})
            break
        # break
    # print(label_list)
    return label_list
def near(doc):
    label_list=[]
    index = -1
    for token in doc:
        index=index+1
        if token.text == "near":
            span=doc[index:-1]
            # print(span.text)
            for ent in span.ents:
                if ent.label_=="FAC":
                    label_list.append({"Near_landmark": ent.text})
                break
        # break
    # print(label_list)
    return label_list
def near_between(doc):
    label_list=[]
    index = -1
    for token in doc:
        index=index+1
        if token.text=="between":
            span=doc[index:-1]
            # print(span.text)
            i=0
            for ent in span.ents:
                if i>1:
                    break
                elif i==0 and ent.label_=="FAC":
                    label_list.append({"Near_landmark": ent.text})
                    i += 1
                elif i == 1 and ent.label_ == "FAC":
                    label_list.append({"Between_landmark": ent.text})
                    i+=1
    # print(label_list)
    return label_list
def parse_matches(doc, matches,label_list):
    start_1 = 0
    count = 1
    string_id_1 = ""
    span_1 = doc
    # lanes =['no. 1', 'middle and slow', 'no. 1, 2 and 3', 'no. 1 and 2', 'tin lok lane', 'no.4,5', 'no. 2 and 3',
    #         'no. 2, 3 and 4', 'no.3,4', 'no.2, 3', 'no.1', 'no.5', 'no.3', 'fast and middle', 'no. 3 and 4', 'no.2',
    #         'no. 2', 'no. 3', 'no. 4', 'no.  3 and 4', 'fast and slow', 'no.3 and 4', 'middle']
    len_orgin=len(label_list)
    FAC=[]
    for ent in doc.ents:
        if ent.label_=="FAC":
            FAC.append(ent.text)
    for match_id, start, end in matches:
        if len(string_id_1) == 0:
            start_1 = start
            string_id_1 = doc.vocab.strings[match_id]  # Get string representation
            span_1 = doc[start:end]  # The matched span
            count = count + 1
        elif start_1 == start and count != len(matches):
            string_id_1 = doc.vocab.strings[match_id]  # Get string representation
            span_1 = doc[start:end]  # The matched span
            count = count + 1
        elif start_1 == start and count == len(matches):
            string_id_1 = doc.vocab.strings[match_id]  # Get string representation
            span_1 = doc[start:end]  # The matched span
            label_list=match_labels(string_id_1, span_1,label_list)
        else:
            label_list=match_labels(string_id_1, span_1,label_list)
            start_1 = start
            string_id_1 = doc.vocab.strings[match_id]  # Get string representation
            span_1 = doc[start:end]  # The matched span
            count = count + 1
    len_update=len(label_list)
    if len_orgin==len_update and len(FAC)!=0:
        label_list.extend(location(doc))
        label_list.extend(direction(doc))
        label_list.extend(near(doc))
        label_list.extend(near_between(doc))
        # for lane in lanes:
        #     if lane in doc.text:
        #         label_list.append({"Lane_landmark": lane})
        #         break

def recursion(token,string=""):
    if len(string) == 0:
        string = token.text
    else:
        string = " ".join((token.text, string))
    list_child = [child for child in token.children]
    if len(list_child)==0:
        return string
    elif len(list_child)==1:
        string=recursion(list_child[0], string)
        return string
    else:
        return string

def parse_incident_cause(doc,label_list):
    len_orgin=len(label_list)
    causes = ['roroad situation', 'hong kong island 10k city race 2019', 'emergency repair of road surface', 'fire', 'rugby matches', 'repair of road surface', 'the situation at university station', 'hong kong cyclothon 2016', 'the preparation works of car racing event', 'repair works', 'red rainstorm warning signal', 'watermain burst', 'event', 'flooding', 'traffic accident', 'actual situation', 'inclement weather', 'construction', 'the car racing event', 'hong kong cyclothon', 'frosting', 'a car racing event', 'strong wind condition', 'emergency incident', 'signalling fault', 'heavy traffic', 'public event', 'damaged traffic lights', 'animal', 'person', 'watermain emergency works', 'tram track renewal works', 'urgent maintenance of the light pole', 'strong wind signal no. 3 and the associated wet weather', 'road subsidence', 'events', 'urgent road works', 'road works', 'person in dangerous position', 'traffic incident', '2016 hong kong cyclothon', 'train fault', 'typhoon', 'mechanical fault', 'wet weather and slippery roads', 'the traffic lights in yau tsim mong district are damaged', 'wall collapsed', 'vehicle breakdown', 'faulty train', 'wet and cold weather', 'fallen tree', 'system failure', 'incident', 'emergency repairing works', 'traffic lights were damaged', 'typhoon no. 8 gale or storm signal', 'the event of cycle for millions', 'funeral ceremony', 'police operation', 'overhead line problem', 'road incident', 'the tai ping ching chiu parades', 'tree collapsed', 'road work', 'typhoon no. 3 strong wind signal and the associated wet  weather', 'vehicle on fire', 'repairing emergency works', 'suspected gas leakage', 'tree trimming', 'flag raising ceremony', 'running race', 'obstacles on roads', 'situation at university station', 'road repairing works', 'equipment fault', 'public procession', 'high wind', 'oil stain on road', 'hong kong streetathon @ kowloon east 2016', 'fire investigation', 'strong wind', 'fallen scaffolding', 'accident', 'improved weather condition', 'the road reinstatement works of a car racing event', 'landslide', 'heavy traffic and the damage of traffic lights', 'hong kong island ,10k city race 2019', 'the access control arrangements at the airport', 'road repair works', 'road situation', 'the foreign object obstructing the overhead line', 'traffic lights under urgent repair', 'power failure', 'obstruction by a fallen tree', 'marathon']
    for token in doc:
        if token.text.lower()=="due":
            list_due_child=[child for child in token.children]
            if len(list_due_child)==1:
                if list_due_child[0].text=="to":
                    list_to_child = [child for child in list_due_child[0].children]
                    if len(list_to_child)==1:
                        cause=recursion(list_to_child[0])
                        if cause!="":
                            label_list.append({"Incident_cause":cause})
                else:
                    cause=recursion(list_due_child[0])
                    if cause!="":
                        label_list.append({"Incident_cause": cause})
            elif len(list_due_child)==2:
                for n in list_due_child:
                    if n.text!="to":
                        cause=recursion(n)
                        if cause!="":
                            label_list.append({"Incident_cause": cause})
    len_update = len(label_list)
    if len_orgin == len_update:
        for cause in causes:
            if cause in doc.text:
                label_list.append({"Incident_cause": cause})
                break
    # return label_list

def parse_states(doc,label_list):
    list_status = []
    list_not_status=['found', 'provide', 'allowed', 'are', 'terminated', 'required', 'announces', 'running', 'advises',
                     'shortened', 'follows', 'restored', 'disrupted', 'routes', 'lifted', 'increased', 'requested',
                     'appeals', 'lanes', 'damaged', 'made', 'section', 'observed', 'blocked', 'anticipated', 'carrying',
                     'strengthened', 'remaining', 'functioning', 'providing', 'adjusting', 'be', 'happened', 'contact',
                     'issued', 'changed', 'broadcast', 'street', 'prohibited', 'end', 'introduced', 'opened', 'will',
                     'operated', 'passing', 'erected', 'expected', 'provided', 'tsing', 'stop', 'ii', 'substituted',
                     'truncated', 'from', 're-routed', 'intervals', 'affected', 'wo', 'bound', '(', 'hung', 'urges',
                     'continue', 'anticipates', 'monitoring', 'located', 'remain', 'lowered', 'to', 'reduced', 'held',
                     'implementing','sent', 'remaining', 'bound', 'tsing', 'happened',"advised","congested","extended",
                     "maintained","implemented"]

    for token in doc:
        if token.lemma_=="be":
            if token.dep_!="ROOT":
                if "which" not in [child.text for child in token.head.children] and token.head.text not in list_not_status:
                    label_list.append({"Status":token.head.text})
                    list_status.append(token.head)
            if token.dep_=="ROOT":
                for child in token.children:
                    if child.pos_=="VERB" \
                            and child.text not in list_not_status:
                        label_list.append({"Status": child.text})
                        list_status.append(child)
    return list_status

def parse_arrangement(doc,list_status,label_list):
    len_orgin=len(label_list)
    arranges=['one-lane-two-way',
               'one-tube-two-way',"speed limit","not stop"]
    for token in list_status:
        for child in token.children:
            if child.pos_ == "VERB" and \
                    "to" in [child.text for child in child.children]:
                for child in child.children:
                    if child.dep_ == "dobj":
                        # print(recursion(child))
                        arrangement = recursion(child)
                        if arrangement != "":
                            label_list.append({"Arrangement": arrangement})
    len_update = len(label_list)
    if len_orgin == len_update:
        for arrange in arranges:
            if arrange in doc.text:
                label_list.append({"Arrangement": arrange})
def parse_re(doc,label_list):
    with open("../data preparation/special corpus/bus company/company_dic.txt", "r") as f:
        BC_list = f.read().splitlines()
        BC_list.append("bus stops")
    with open("../data preparation/special corpus/subway line/subway_line.txt", "r") as f:
        SL_list = f.read().splitlines()
        SL_list.extend(['kwun tong line', 'light rail', 'east rail line', 'train service', 'airport express', 'west rail line'])
        SL_list = list(set(SL_list))
    with open("../data preparation/special corpus/ferry line/ferry_dic.txt", "r", encoding="utf-8") as f:
        FL_list = f.read().splitlines()
        FL_list.extend(['ferry service','central to cheung chau',"macau ferry","kwun tong ferry","north point ferry"])
        FL_list = list(set(FL_list))
    with open("../data preparation/special corpus/tram line/tram_dic.txt", "r", encoding="utf-8") as f:
        TL_list = f.read().splitlines()
        TL_list.extend(['tramway services', 'happy valley loop', 'peak tram', 'west bound tramway',
                        'eastbound tram', 'westbound tramway', 'east bound tramway', 'happy valley loop tram'])
        TL_list = list(set(TL_list))
    for BC in ['s1 and s64', '87k, 87s, 272a, 272k, 289k', 'k12, k17, k18 and b1', 'b3m', '37, 37m and 38', 'db03p, db02a',
               'k12, k17 and k18', '260', '73x, 74d, 213m, 272s, 274p, b5', 'db02r', '1, 2, 3m, 4, 11, 21, 23, 34, 36, 37h, b2 and b2p',"bus stops"]:
        if BC in doc.text:
            label_list.append({"Bus": BC})
    for BC in BC_list:
        if BC in doc.text:
            expression = r'\d\d*[A-Z]*'
            bus = ""
            for match in re.finditer(expression, doc.text):
                start, end = match.span()
                span = doc.char_span(start, end)
                # This is a Span object or None if match doesn't map to valid token sequence
                if span is not None:
                    # print("Found match:", span.text)
                    if bus=="":
                        bus=span.text
                    else:
                        bus=bus+", "+span.text
            if bus!="":
                label_list.append({"Bus":bus})
    for SL in SL_list:
        if SL in doc.text:
            label_list.append({"Subway": SL})
    for FL in FL_list:
        if FL in doc.text:
            label_list.append({"Ferry":FL})
    for TL in TL_list:
        if TL in doc.text:
            label_list.append({"Tram":TL})

def parse_text(text,nlp,label_list):
    doc=nlp(text)
    matches=matcher(doc)
    # parse_arrangement(doc,label_list)
    try:
        parse_incident_cause(doc,label_list)
        list_status=parse_states(doc, label_list)
        parse_matches(doc, matches,label_list)
        parse_arrangement(doc,list_status, label_list)
        parse_re(doc, label_list)
        # return label_list
    except:
        pass

        # return label_list
def save_json(path,df):
    print("parsing dataframe")
    with open(path, "a")as f:
        for index, row in df.iterrows():
            print("parsing %s"%index)
            label_list = []
            text = row["Text"]
            parse_text(text,nlp,label_list)
            if row["Date"] is not pd.NaT:
                jsonData = json.dumps(
                    {'index': index, 'text': row["Text"], 'date': str(row["Date"]), 'label_list': label_list}, indent=4)
                f.write(jsonData + "\n")
            if row["Date"] is pd.NaT:
                jsonData = json.dumps({'index': index, 'text': row["Text"], 'label_list': label_list}, indent=4)
                f.write(jsonData + "\n")

if __name__ == "__main__":
    df1 = pd.read_csv("../data preparation/tn_1st_dump.csv", header=0, index_col=0)
    df2 = pd.read_csv("../data preparation/tn_2nd_dump.csv", header=0, index_col=0)
    path1="parse_1st.json"
    path2="parse_2nd.json"
    save_json(path1, df1)
    save_json(path2, df2)

