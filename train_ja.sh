#!usr/bin/env bash

CUDA_VISIBLE_DEVICES=1 \
python run_translation.py \
    --model_name_or_path facebook/mbart-large-50-one-to-many-mmt \
    --do_train \
    --do_eval \
    --source_lang en_XX \
    --target_lang ja_XX \
    --train_file /raid/ieda/trans_jaen_dataset/Dataset/data_sources/data_bt/json_style/train.jsonl\
    --validation_file /raid/ieda/trans_jaen_dataset/Dataset/data_sources/data_bt/json_style/val.jsonl\
    --output_dir /raid/ieda/examples_result/rensyu2 \
    --per_device_train_batch_size=16 \
    --per_device_eval_batch_size=16 \
    --overwrite_output_dir \
    --num_train_epochs 2 \
    --save_strategy epoch \
    --predict_with_generate \
    --seed 42 #\
    # --enable_peft
# for changing evaluation timing, --evaluation_strategy step and --eval_steps 1000 or like that
# --seed 42