#!usr/bin/env bash

CHECKPOINT=109
MODEL_DIR=mbart_parallel_only

CUDA_VISIBLE_DEVICES=1 \
python run_translation.py \
    --model_name_or_path /raid/ieda/examples_result/${MODEL_DIR}/checkpoint-${CHECKPOINT} \
    --do_predict \
    --source_lang en_XX \
    --target_lang ja_XX \
    --forced_bos_token ja_XX \
    --test_file /raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/test.jsonl\
    --output_dir /raid/ieda/examples_result/${MODEL_DIR}/result-${CHECKPOINT} \
    --overwrite_output_dir \
    --predict_with_generate \
    --seed 42 #\
