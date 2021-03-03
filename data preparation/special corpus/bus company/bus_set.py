import xml.etree.ElementTree as ET


if __name__ == '__main__':
    file_path = 'COMPANY_CODE.xml'
    tree = ET.parse(file_path)
    root = tree.getroot()
    for child in root:
        for child in child:
            if child.tag=="COMPANY_NAMEE" and child.text not in ["FERRY", "TRAM","PTRAM"]:
                with open("company_dic_title", "a") as f:
                    f.write(child.text + "\n")
