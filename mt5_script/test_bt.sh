#!usr/bin/env bash

TESTSET_VER=test # val, test
CHECKPOINT=253380 #202704,228042,253380
MODEL_DIR=mt5_bt_pre_finetuned

CUDA_VISIBLE_DEVICES=0 \
python run_translation.py \
    --model_name_or_path /raid/ieda/examples_result/${MODEL_DIR}/checkpoint-${CHECKPOINT} \
    --do_predict \
    --source_lang en_XX \
    --target_lang ja_XX \
    --forced_bos_token ja_XX \
    --test_file /raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/${TESTSET_VER}.jsonl\
    --output_dir /raid/ieda/examples_result/${MODEL_DIR}/${TESTSET_VER}result-${CHECKPOINT} \
    --overwrite_output_dir \
    --predict_with_generate \
    --seed 42 #\
