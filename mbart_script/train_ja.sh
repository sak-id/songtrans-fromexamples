#!usr/bin/env bash

CUDA_VISIBLE_DEVICES=0 \
python run_translation.py \
    --model_name_or_path facebook/mbart-large-50-one-to-many-mmt \
    --do_train \
    --do_eval \
    --source_lang en_XX \
    --target_lang ja_XX \
    --train_file /raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/train.jsonl\
    --validation_file /raid/ieda/trans_jaen_dataset/Data/json_datasets/data_parallel/val.jsonl\
    --output_dir /raid_elmo/home/lr/ieda/examples_result/mbart_parallel_only \
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
    --logging_steps 50 
    # --enable_peft