#!usr/bin/env bash

CUDA_VISIBLE_DEVICES=1 \
python run_translation.py \
    --model_name_or_path facebook/mbart-large-50-one-to-many-mmt \
    --do_predict \
    --source_lang en_XX \
    --target_lang ja_XX \
    --test_file /raid/ieda/trans_jaen_dataset/Dataset/data_sources/data_bt/json_style/test.jsonl\
    --output_dir /raid/ieda/examples_result/rensyu_result_secondtest \
    --overwrite_output_dir \
    --predict_with_generate \
    --seed 42 \
    --enable_peft \
    --peft_path /raid/ieda/examples_result/rensyu/checkpoint-209/
