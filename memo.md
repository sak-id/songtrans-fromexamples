# 実行したもの

基本raidにしまう

| モデル | Lora | 事前学習済み | データセット | スクリプト | 保存場所 | 備考 |
| ---- |----|----|----|----|---- | ---- |
| mBART | False | No | parallel | train_ja.sh |raid_elmo/home/lr/ieda/example_result/mbart_parallel_only| データシャッフル前|
| mBART | True | No | parallel | train_peft.sh | raid/ieda/example_result/lora_parallel_only| データシャッフル前 |
| mBART | False | No | bt | train_bt.sh | raid/ieda/examples_result/mbart_bt_pre_finetuned | |
| mBART | False |No | parallel | train_parallel_only.sh | | |
| mBART | True |No | parallel | train_peft_parallel_only.sh | | |





### データセット
|データセット名|内容|
|-- | -- |
|bt | RWC+クローリングデータと逆翻訳による翻訳対<br>事前学習に用いる |
|parallel | 英日クローリングして人手で行を揃えた対訳データ |