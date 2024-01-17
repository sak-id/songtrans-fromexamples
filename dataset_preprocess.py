import os
import json
import pandas as pd
parallel_path = '/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_bt/full.jsonl'
output_dir = '/raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel'
input_dir = '/raid/ieda/trans_jaen_dataset/Data/source_data/data_parallel'
def main():
    text_devide_to_train_val_test("json")
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
    full_parallel = load_data(parallel_path)
    len_parallel = len(full_parallel)
    print(f"{len_parallel} lines")
    train_data = full_parallel[:-1000]
    val_data = full_parallel[-1000:]
    print(f"train: {len(train_data)} lines")
    print(f"val: {len(val_data)} lines")
    breakpoint()
    save_data(train_data, os.path.join(output_dir, 'train.jsonl'))
    save_data(val_data, os.path.join(output_dir, 'val.jsonl'))

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


# def json_devide_to_train_val_test():
#     full_parallel = load_data(parallel_path)
#     len_parallel = len(full_parallel)
#     train_data = full_parallel[:int(len_parallel*0.8)]
#     val_data = full_parallel[int(len_parallel*0.8):int(len_parallel*0.9)]
#     test_data = full_parallel[int(len_parallel*0.9):]
#     print(f"train: {len(train_data)} lines")
#     print(f"val: {len(val_data)} lines")
#     breakpoint()
#     save_data(train_data, os.path.join(output_dir, 'train.jsonl'))
#     save_data(val_data, os.path.join(output_dir, 'val.jsonl'))
#     save_data(test_data, os.path.join(output_dir, 'test.jsonl'))

def load_data(data_path):
    with open(data_path, 'r') as f:
        data = f.readlines()
    return data

def save_data(data, save_path):
    with open(save_path, 'w') as f:
        f.writelines(data)

if __name__ == '__main__':
    main()