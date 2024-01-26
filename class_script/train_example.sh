dataset="reuters21578"
subset="ModApte"
python run_classification.py \
    --model_name_or_path bert-base-uncased \
    --dataset_name ${dataset} \
    --dataset_config_name ${subset} \
    --shuffle_train_dataset \
    --remove_splits "unused" \
    --metric_name f1 \
    --text_column_name text \
    --label_column_name topics \
    --do_train \
    --do_eval \
    --max_seq_length 512 \
    --per_device_train_batch_size 32 \
    --learning_rate 2e-5 \
    --num_train_epochs 15 \
    --output_dir /raid/ieda/lyric_classifier/${dataset}_${subset}/ \
    --evaluation_strategy epoch \
    --save_strategy epoch \
    --save_total_limit 2 \
    --report_to tensorboard \
    --logging_steps epoch \
    --seed 42 

# change cache dir