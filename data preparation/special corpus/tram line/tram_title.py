with open('tram_dic.txt',"r",encoding="utf-8") as f,\
         open("tram_dic_title.txt","a+",encoding="utf-8") as f1:
    orig = f.read().splitlines()
    for line in orig:
        f1.write(line.title() + "\n")