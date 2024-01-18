#!usr/bin/env bash

OUTPUT_DIR=mt5_peft_parallel_only

CUDA_VISIBLE_DEVICES=1 \
python run_translation.py \
    --model_name_or_path google/mt5-base \
    --do_train \
    --do_eval \
    --source_lang en_XX \
    --target_lang ja_XX \
    --train_file /raid/ieda/trans_jaen_dataset/Dataset/datasets/data_parallel/train.jsonl\
    --validation_file /raid/ieda/trans_jaen_dataset/Dataset/datasets/data_parallel/val.jsonl\
    --output_dir /raid/ieda/examples_result/${OUTPUT_DIR} \
    --forced_bos_token ja_XX \
    --per_device_train_batch_size=16 \
    --per_device_eval_batch_size=16 \
    --overwrite_output_dir \
    --num_train_epochs 10 \
    --save_strategy epoch \
    --predict_with_generate \
    --evaluation_strategy epoch\
    --seed 42 \
    --report_to tensorboard \
    --logging_steps 50 \
    --logging_first_step \
    --enable_peft
