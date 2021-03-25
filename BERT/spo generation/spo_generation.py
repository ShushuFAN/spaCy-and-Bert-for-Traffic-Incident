import json

def affect(subject,object):
    global spo_list
    spo_list.append({"predicate": "Affect", "subject": subject, "object": object})
def status(subject,object):
    global spo_list
    spo_list.append({"predicate": "Status", "subject": subject, "object": object})
def lane(object):
    global dic,spo_list
    if len(dic["Lane_landmark"]) != 0:
        Lane_landmark = dic["Lane_landmark"].pop(0)
        spo_list.append({"predicate": "Lane", "subject": Lane_landmark, "object": object})
def near_between_direction(object):
    global dic,spo_list
    if len(dic["Direction_landmark"]) != 0:
        Direction_landmark = dic["Direction_landmark"].pop(0)
        spo_list.append({"predicate": "Direction", "subject": Direction_landmark, "object": object})
    if len(dic["Near_landmark"]) != 0:
        Near_landmark = dic["Near_landmark"].pop(0)
        spo_list.append({"predicate": "Near", "subject": Near_landmark, "object": object})
    if len(dic["Between_landmark"]) != 0:
        Between_landmark = dic["Between_landmark"].pop(0)
        spo_list.append({"predicate": "Between", "subject": Between_landmark, "object": object})
def arrangement(subject):
    global dic,spo_list
    if len(dic["Arrangement"]) != 0:
        Arrangement = dic["Arrangement"].pop(0)
        spo_list.append({"predicate": "Arrangement", "subject": subject, "object": Arrangement})
        if len(dic["Location"]) != 0:
            Location = dic["Location"].pop(0)
            spo_list.append(
                {"predicate": "Location", "subject": Arrangement, "object": Location})
            near_between_direction(Arrangement)
def public_transport_parse(list_transport):
    global dic,spo_lis
    while len(dic["Status"]) > 1:
        public_transport = list_transport.pop(0)
        Status = dic["Status"].pop(0)
        spo_list.append({"predicate": "Status", "subject": public_transport, "object": Status})
        near_between_direction(public_transport)
        arrangement(Status)
    for public_transport in list_transport:
        spo_list.append({"predicate": "Status", "subject": public_transport, "object": dic["Status"][0]})
        near_between_direction(public_transport)
        arrangement(dic["Status"][0])
def append_spo(label_list):
    global dic,spo_list
    dic={"Incident_cause":[],"Status":[],"Lane_landmark":[],"Location":[],"Direction_landmark":[],"Near_landmark":[],
         "Between_landmark":[],"Arrangement":[],"Bus":[],"Subway":[],"Ferry":[],"Tram":[],"Light_rail":[]}
    spo_list=[]
    for label in label_list:
        for label_name in dic.keys():
            if label_name in label:
                dic[label_name].append(label[label_name])
    n_status=len(dic["Status"])
    n_location=len(dic["Location"])
    if len(dic["Incident_cause"])!=0 and dic["Incident_cause"]!=["heavy traffic"]:
    # if len(dic["Incident_cause"]) != 0:
        Incident_cause=dic["Incident_cause"][0]
        public_transport_labels=["Bus","Subway","Ferry","Tram","Light_rail"]
        for transport in public_transport_labels:
            for Object in dic[transport]:
                affect(Incident_cause, Object)
        global list_transport
        list_transport=dic["Bus"]+dic["Subway"]+dic["Ferry"]+dic["Tram"]+dic["Light_rail"]
        n_transport=len(list_transport)
        if 0<n_status<=n_transport:
            # print("if1")
            public_transport_parse(list_transport)
        elif 0<n_transport < n_status <= n_transport+n_location:
            # print("if2")
            while len(dic["Status"]) > max(n_transport,1):
                Location=dic["Location"].pop(0)
                affect(Incident_cause, Location)
                Status=dic["Status"].pop(0)
                status(Location, Status)
                lane(Location)
                near_between_direction(Location)
            if len(dic["Status"])==n_transport:
                public_transport_parse(list_transport)
            elif len(dic["Status"])==1:
                for public_transport in list_transport:
                    status(public_transport, dic["Status"][0])
                    near_between_direction(public_transport)
                    arrangement(dic["Status"][0])
        elif n_transport <= n_transport+n_location < n_status :
            # print("if3")
            status(Incident_cause, dic["Status"].pop(0))
            while len(dic["Location"]) > 0:
                Location=dic["Location"].pop(0)
                affect(Incident_cause, Location)
                Status=dic["Status"].pop(0)
                status(Location, Status)
                lane(Location)
                near_between_direction(Location)
            while len(list_transport)>0:
                public_transport = list_transport.pop(0)
                Status = dic["Status"].pop(0)
                status(public_transport, Status)
                near_between_direction(public_transport)
                arrangement(Status)
        elif n_transport==0 and 0<n_status<=n_location:
            # print("if4")
            while len(dic["Status"]) > 1:
                Location=dic["Location"].pop(0)
                affect(Incident_cause, Location)
                Status=dic["Status"].pop(0)
                status(Location, Status)
                lane(Location)
                near_between_direction(Location)
            for Location in dic["Location"]:
                affect(Incident_cause, Location)
                status(Location, dic["Status"][0])
                lane(Location)
                near_between_direction(Location)
        elif n_transport==n_location==0 and n_status!=0:
            # print("if5")
            while len(dic["Status"]) > 0:
                Status = dic["Status"].pop(0)
                status(Incident_cause, Status)
        elif n_status==0:
            # print("if6")
            arrangement(Incident_cause)
            while len(dic["Location"]) > 0:
                Location=dic["Location"].pop(0)
                affect(Incident_cause, Location)
                lane(Location)
                near_between_direction(Location)
        # else:
        #     print("else")
    return spo_list




def generate_spo(file,n):
    with open(file,"r",encoding='utf-8') as f:
        record = ""
        global index_new
        for line in f:
            if line == "{\n" or line == "{":
                record = record + line
            elif line == "}\n" or line == "}":
                record = record + line
                json_info = json.loads(record)
                index=json_info["index"]
                print(index)
                if index<n+1:
                    label_list=json_info["label_list"]
                    spo_list=append_spo(label_list)
                    # print(spo_list)
                    # with open("spo_generation.json", "a")as f:
                    #     jsonData = json.dumps({'index_new': index_new, 'source': file, 'index_orig': index,
                    #                            'text': json_info["text"], 'label_list': spo_list},
                    #                           indent=4)
                    #     f.write(jsonData + "\n")
                    #     index_new += 1
                    if len(spo_list)!=0:
                        with open("spo_generation.json", "a")as f1:
                            jsonData = json.dumps({'index_new': index_new, 'source': file, 'index_orig': index,
                                                   'text': json_info["text"], 'spo_list': spo_list},
                                                  indent=4)
                            f1.write(jsonData + "\n")
                            index_new+=1
                else:
                    break
                record = ""
            elif line == "\n":
                pass
            else:
                record = record + line

if __name__ == '__main__':
    label_filename_1 = "parse_1st_revise.json"
    label_filename_2 = "parse_2nd_revise.json"
    # n_checked=515
    index_new=0
    global dic, spo_list,list_transport
    generate_spo(label_filename_1, 4789)
    generate_spo(label_filename_2, 8965)

    # generate_spo(label_filename_1, 13)