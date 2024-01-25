import os
import json
import pandas as pd
# parallel_path = '/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_bt/full.jsonl'
output_dir = '/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel'
input_dir = '/raid/ieda/trans_jaen_dataset/Data/source_data/data_parallel'
def main():
    # full_train = load_csv(input_dir + '/jpop_train.csv')
    # shuffle_json_to_train_val(full_train,os.path.join(output_dir, 'train.jsonl'))
    # full_val = load_csv(input_dir + '/jpop_val.csv')
    # shuffle_json_to_train_val(full_val,os.path.join(output_dir, 'val.jsonl'))
    full_test = load_csv(input_dir + '/test.csv')
    shuffle_json_to_train_val(full_test,os.path.join(output_dir, 'test.jsonl'))
    pass

# for bt data
def text_devide_to_train_val():
    full_source = load_data(input_dir + '/full.source')
    full_target = load_data(input_dir + '/full.target')
    len_source = len(full_source)
    len_target = len(full_target)
    assert len_source == len_target
    print(f"{len_source} lines")
    train_source = full_source[:-1000]
    train_target = full_target[:-1000]
    val_source = full_source[-1000:]
    val_target = full_target[-1000:]
    print(f"train: {len(train_source)} lines")
    print(f"val: {len(val_source)} lines")
    assert len(train_source) == len(train_target)
    assert len(val_source) == len(val_target)
    breakpoint()
    save_data(train_source, os.path.join(output_dir, 'train.source'))
    save_data(train_target, os.path.join(output_dir, 'train.target'))
    save_data(val_source, os.path.join(output_dir, 'val.source'))
    save_data(val_target, os.path.join(output_dir, 'val.target'))

# for bt data
def json_devide_to_train_val():
    # full_parallel = load_data(parallel_path)
    # len_parallel = len(full_parallel)
    full_source = load_data(input_dir + '/full.source')
    full_target = load_data(input_dir + '/full.target')
    len_source = len(full_source)
    len_target = len(full_target)
    assert len_source == len_target
    print(f"{len_source} lines")
    train_source = full_source[:-1000]
    train_target = full_target[:-1000]
    val_source = full_source[-1000:]
    val_target = full_target[-1000:]
    print(f"train: {len(train_source)} lines")
    print(f"val: {len(val_source)} lines")
    assert len(train_source) == len(train_target)
    assert len(val_source) == len(val_target)
    breakpoint()
    with open(output_dir + "/train.jsonl","w") as f:
        for en_text,ja_text in zip(train_source,train_target):
            f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
            f.write("\n")
    with open(output_dir + "/val.jsonl","w") as f:
        for en_text,ja_text in zip(val_source,val_target):
            f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
            f.write("\n")
    # print(f"{len_parallel} lines")
    # train_data = full_parallel[:-1000]
    # val_data = full_parallel[-1000:]
    # print(f"train: {len(train_data)} lines")
    # print(f"val: {len(val_data)} lines")
    # breakpoint()
    # save_data(train_data, os.path.join(output_dir, 'train.jsonl'))
    # save_data(val_data, os.path.join(output_dir, 'val.jsonl'))

# for parallel data
def text_devide_to_train_val_test(mode): # mode: text or json
    full_source = load_data(input_dir + '/shuffled_full.source')
    full_target = load_data(input_dir + '/shuffled_full.target')
    len_source = len(full_source)
    len_target = len(full_target)
    assert len_source == len_target
    print(f"{len_source} lines")
    print("full_source & full_target already shuffled?")
    breakpoint()
    train_source = full_source[:int(len_source*0.8)]
    train_target = full_target[:int(len_target*0.8)]
    val_source = full_source[int(len_source*0.8):int(len_source*0.9)]
    val_target = full_target[int(len_target*0.8):int(len_target*0.9)]
    test_source = full_source[int(len_source*0.9):]
    test_target = full_target[int(len_target*0.9):]
    print(f"train: {len(train_source)} lines")
    print(f"val: {len(val_source)} lines")
    assert len(train_source) == len(train_target)
    assert len(val_source) == len(val_target)
    if mode=="text":
        save_data(train_source, os.path.join(output_dir, 'train.source'))
        save_data(train_target, os.path.join(output_dir, 'train.target'))
        save_data(val_source, os.path.join(output_dir, 'val.source'))
        save_data(val_target, os.path.join(output_dir, 'val.target'))
        save_data(test_source, os.path.join(output_dir, 'test.source'))
        save_data(test_target, os.path.join(output_dir, 'test.target'))
    elif mode=="json":
        with open(output_dir + "/train.jsonl","w") as f:
            for en_text,ja_text in zip(train_source,train_target):
                f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
                f.write("\n")
        with open(output_dir + "/val.jsonl","w") as f:
            for en_text,ja_text in zip(val_source,val_target):
                f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
                f.write("\n")
        with open(output_dir + "/test.jsonl","w") as f:
            for en_text,ja_text in zip(test_source,test_target):
                f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
                f.write("\n")
    else:
        raise ValueError("mode must be text or json")

# for parallel data
def do_shuffle():
    full_source = load_data(input_dir + '/full.source')
    full_target = load_data(input_dir + '/full.target')
    len_source = len(full_source)
    len_target = len(full_target)
    assert len_source == len_target
    print(f"{len_source} lines")
    df = pd.DataFrame({'source': full_source, 'target': full_target})
    df = df.sample(frac=1, random_state=42)
    full_source = df['source'].tolist()
    full_target = df['target'].tolist()
    with open(os.path.join(output_dir, 'shuffled_full.source'), 'w') as f:
        f.writelines(full_source)
    with open(os.path.join(output_dir, 'shuffled_full.target'), 'w') as f:
        f.writelines(full_target)


def shuffle_json_to_train_val(df_data,output_path):
    # shuffle, then save as jsonl
    assert type(df_data)==pd.core.frame.DataFrame
    df_data = df_data.sample(frac=1, random_state=42)
    with open(output_path,"w") as f:
        for en_text,ja_text in zip(df_data['en'],df_data['ja']):
            f.write(json.dumps({"translation": {"en":en_text.strip("\n"),"ja":ja_text.strip("\n").strip("　")}},ensure_ascii=False))
            f.write("\n")


def load_csv(input_path):
    df = pd.read_csv(input_path)
    en_text = df.iloc[0]['en'].split("\n")
    ja_text = df.iloc[0]['ja'].split("\n")
    new_df = pd.DataFrame(columns=['en', 'ja'])
    for i in range(1,len(df)):
        # 曲ごとに英語歌詞・日本語歌詞を取得
        en_text = df.iloc[i]['en'].split("\n")
        ja_text = df.iloc[i]['ja'].split("\n")
        # new_dfに追加
        tmp_df = pd.DataFrame({'en': en_text, 'ja': ja_text})
        new_df = pd.concat([new_df, tmp_df])
    return new_df

def load_data(data_path):
    with open(data_path, 'r') as f:
        data = f.readlines()
    return data

def save_data(data, save_path):
    with open(save_path, 'w') as f:
        f.writelines(data)

if __name__ == '__main__':
    main()