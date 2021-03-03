with open('road_dic.txt',"r") as f,\
         open('road_dic_title.txt',"a+") as f1:
    orig = f.read().splitlines()
    for line in orig:
        f1.write(line.title() + "\n")