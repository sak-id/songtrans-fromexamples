#!usr/bin/env bash

PRETRAINED_MODEL_DIR=/raid/ieda/examples_result/mbart_bt_pre_finetuned/checkpoint-50676
MERGE_RATE=0.7

TEST_DATASET=test # test or nursery


CUDA_VISIBLE_DEVICES=1 \
python run_translation.py \
    --model_name_or_path $PRETRAINED_MODEL_DIR \
    --do_predict \
    --source_lang en_XX \
    --target_lang ja_XX \
    --forced_bos_token ja_XX \
    --test_file /raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/test_not_shuffle.jsonl\
    --output_dir ./genre_results/Musical${MERGE_RATE}_${TEST_DATASET} \
    --overwrite_output_dir \
    --predict_with_generate \
    --seed 42 \
    --enable_peft \
    --merge_two_adapters \
    --merge_rate $MERGE_RATE 