import json
import os
import re
import csv
import pandas as pd


# convert to jsonl format
# {"translation": {"en": "I am a student.", "zh": "我是一名学生。"}}
en_input_path = "/raid/ieda/trans_jaen_dataset/Data/source_data/data_bt/full.source"
ja_input_path = "/raid/ieda/trans_jaen_dataset/Data/source_data/data_bt/full.target"

output_path = "/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_bt/full.jsonl"

# csvの場合
# source = []
# with open(en_input_path,"r") as f:
#     reader = csv.reader(f)
#     for i in reader:
#         source.extend(i[1].split("\n"))
# target = []
# with open(ja_input_path,"r") as f:
#     reader = csv.reader(f)
#     for i in reader:
#         target.extend(i[1].split("\n"))
# textの場合
with open(en_input_path,"r") as f:
    source = f.readlines()
with open(ja_input_path,"r") as f:
    target = f.readlines()
l = []
for i in range(len(source)):
    # if re.search(r'[a-zA-Zａ-ｚＡ-Ｚ0-9０-９]',target[i])!=None: # 英語が含まれるならskip
    #     continue
    # source[i] = re.sub(r"\(\w+\)|\(\w+\）|\（\w+\）|\（\w+\)|\[\w+\]|\【\w+\】" ,"", source[i].strip("\n")) 
    source[i] = re.sub(r"[\",.!?]","",source[i]) # 英語のダブルクォーテーションを消す
    target[i] = re.sub(r"[\s]+","",target[i]) # 日本語の空白を消す
    l.append([source[i],target[i]])
df = pd.DataFrame(l,columns=["en","ja"])
df = df.drop_duplicates()

breakpoint()
flag = False
with open(output_path,"w") as f:
    for en_text,ja_text in df.values:
        if not flag:
            flag = True
            continue
        f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
        f.write("\n")