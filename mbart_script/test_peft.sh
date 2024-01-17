#!usr/bin/env bash

CUDA_VISIBLE_DEVICES=0 \
python run_translation.py \
    --model_name_or_path facebook/mbart-large-50-one-to-many-mmt \
    --do_predict \
    --source_lang en_XX \
    --target_lang ja_XX \
    --forced_bos_token ja_XX \
    --test_file /raid/ieda/trans_jaen_dataset/Dataset/datasets/data_parallel/test.jsonl\
    --output_dir /raid/ieda/examples_result/lora_parallel_only/result-648 \
    --overwrite_output_dir \
    --predict_with_generate \
    --seed 42 \
    --enable_peft \
    --peft_path /raid/ieda/examples_result/lora_parallel_only/checkpoint-648/
