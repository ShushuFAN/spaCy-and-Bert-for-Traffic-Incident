import json
import random
with open("dataset.json", "r") as f, \
        open("test.json", "a+") as f1:
    orig = f.read().splitlines()
    test = random.sample(orig, int(len(orig) * 0.3))
    for line in test:
        json_line = json.loads(line)
        json.dump(json_line, f1)
        f1.write("\n")