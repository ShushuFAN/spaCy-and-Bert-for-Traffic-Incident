with open('subway_line.txt',"r") as f,\
         open("subway_line_title.txt","a+") as f1:
    orig = f.read().splitlines()
    for line in orig:
        f1.write(line.title() + "\n")