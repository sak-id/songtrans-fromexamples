import os
parallel_path = '/raid/ieda/trans_jaen_dataset/Dataset/data_sources/data_parallel/parallel.jsonl'
output_dir = '/raid/ieda/trans_jaen_dataset/Dataset/datasets/data_parallel'
def main():
    full_parallel = load_data(parallel_path)
    len_parallel = len(full_parallel)
    train_data = full_parallel[:int(len_parallel*0.8)]
    val_data = full_parallel[int(len_parallel*0.8):int(len_parallel*0.9)]
    test_data = full_parallel[int(len_parallel*0.9):]
    save_data(train_data, os.path.join(output_dir, 'train.jsonl'))
    save_data(val_data, os.path.join(output_dir, 'val.jsonl'))
    save_data(test_data, os.path.join(output_dir, 'test.jsonl'))
    pass

def load_data(data_path):
    with open(data_path, 'r') as f:
        data = f.readlines()
    return data

def save_data(data, save_path):
    with open(save_path, 'w') as f:
        f.writelines(data)

if __name__ == '__main__':
    main()