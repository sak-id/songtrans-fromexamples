#!usr/bin/env bash

PRETRAINED_MODEL_DIR=/raid/ieda/examples_result/mt5_bt_pre_finetuned/checkpoint-253380
CHECKPOINT=1090 #218
MODEL_DIR=mt5_peft_parallel_after_bt

CUDA_VISIBLE_DEVICES=0 \
python run_translation.py \
    --model_name_or_path $PRETRAINED_MODEL_DIR \
    --do_predict \
    --source_lang en_XX \
    --target_lang ja_XX \
    --forced_bos_token ja_XX \
    --test_file /raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/test.jsonl\
    --output_dir /raid/ieda/examples_result/${MODEL_DIR}/result-${CHECKPOINT} \
    --overwrite_output_dir \
    --predict_with_generate \
    --seed 42 \
    --enable_peft \
    --peft_path /raid/ieda/examples_result/${MODEL_DIR}/checkpoint-${CHECKPOINT}/

