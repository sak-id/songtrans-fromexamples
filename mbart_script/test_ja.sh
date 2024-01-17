#!usr/bin/env bash

CUDA_VISIBLE_DEVICES=1 \
python run_translation.py \
    --model_name_or_path /raid_elmo/home/lr/ieda/examples_result/mbart_parallel_only/checkpoint-540 \
    --do_predict \
    --source_lang en_XX \
    --target_lang ja_XX \
    --forced_bos_token ja_XX \
    --test_file /raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/test.jsonl\
    --output_dir /raid_elmo/home/lr/ieda/examples_result/mbart_parallel_only/result-540 \
    --overwrite_output_dir \
    --predict_with_generate \
    --seed 42 #\
