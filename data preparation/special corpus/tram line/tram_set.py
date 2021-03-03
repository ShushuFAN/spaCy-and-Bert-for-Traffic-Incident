import xml.etree.ElementTree as ET


if __name__ == '__main__':
    file_path = 'ROUTE_TRAM.xml'
    tree = ET.parse(file_path)
    root = tree.getroot()
    for child in root:
        for child in child:
            if child.tag=="ROUTE_NAMEE":
                with open("tram_dic.txt", "a", encoding="utf-8") as f:
                    f.write(child.text.lower() + "\n")