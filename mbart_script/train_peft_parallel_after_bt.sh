#!usr/bin/env bash

MODEL_DIR=/raid/ieda/examples_result/mbart_bt_pre_finetuned/checkpoint-50676
OUTPUT_DIR=mbart_peft_parallel_after_bt

CUDA_VISIBLE_DEVICES=0 \
python run_translation.py \
    --model_name_or_path $MODEL_DIR \
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
