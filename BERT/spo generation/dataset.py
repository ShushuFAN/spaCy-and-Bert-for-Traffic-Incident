import json


def divert(file):
    with open(file, "r", encoding='utf-8') as f:
        record = ""
        for line in f:
            if line == "{\n" or line == "{":
                record = record + line.replace("\n","")
            elif line == "}\n" or line == "}":
                record = record + line.replace("\n","")
                json_info = json.loads(record)
                index = json_info["index_new"]
                with open("dataset.json", "a")as f1:
                    jsonData = json.dumps(json_info)
                    f1.write(jsonData + "\n")
                    print(index)
                record = ""
            elif line == "\n":
                pass
            else:
                record = record + line.replace("\n","")
if __name__ == '__main__':
    dataset_orig = "spo_revise.json"
    divert(dataset_orig)
