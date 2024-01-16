#!usr/bin/env bash

CUDA_VISIBLE_DEVICES=1 \
python run_translation.py \
    --model_name_or_path /raid/ieda/examples_result/mbart1/checkpoint-1080 \
    --do_predict \
    --source_lang en_XX \
    --target_lang ja_XX \
    --forced_bos_token ja_XX \
    --test_file /raid/ieda/trans_jaen_dataset/Dataset/datasets/data_parallel/test.jsonl\
    --output_dir /raid/ieda/examples_result/mbart1_result2 \
    --overwrite_output_dir \
    --predict_with_generate \
    --seed 42 #\
