import json
import hashlib

with open("/content/drive/MyDrive/main_news_mirror.json") as f:
    a = json.load(f)
with open("/content/drive/MyDrive/main_news_mirror_fix.json") as f:
    b = json.load(f)

ids = list()
b_ids = list()
for i in a:
    if len(i["content"].strip()) != 0:
        hash_seed = i["title"] + i["content"] + i["date"]
    else:
        hash_seed = i["title"]
    id = hashlib.sha256(hash_seed.encode('utf-8')).hexdigest()

    ids.append(id)

for i in b:
    b_ids.append(i["id"])

for i in ids:
    if i not in b_ids:
        print(i)

