#!usr/bin/env bash

# bt pre-training for genre adaption
CUDA_VISIBLE_DEVICES=0 \
python run_translation.py \
    --model_name_or_path facebook/mbart-large-50-one-to-many-mmt \
    --do_train \
    --do_eval \
    --source_lang en_XX \
    --target_lang ja_XX \
    --train_file /raid/ieda/trans_jaen_dataset/Data/json_datasets/data_crawled/train.jsonl\
    --validation_file /raid/ieda/trans_jaen_dataset/Data/json_datasets/data_crawled/val.jsonl\
    --output_dir /raid/ieda/examples_result/mbart_bt_pre_for_genre \
    --forced_bos_token ja_XX \
    --per_device_train_batch_size=32 \
    --per_device_eval_batch_size=32 \
    --overwrite_output_dir \
    --num_train_epochs 10 \
    --save_strategy epoch \
    --predict_with_generate \
    --evaluation_strategy steps\
    --eval_steps  0.025\
    --seed 42 \
    --report_to tensorboard \
    --logging_steps  0.025