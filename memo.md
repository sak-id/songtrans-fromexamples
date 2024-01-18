# 実行したもの

基本raidにしまう

| モデル | Lora | 事前学習済み | データセット | スクリプト | 保存場所 | 備考 |
| ---- |----|----|----|----|---- | ---- |
| mBART | False | False | 学習なし | test_pretrained.sh | raid pretrained_model_result | 学習前のtest |
| mBART | False | No | parallel | train_ja.sh |raid_elmo mbart_parallel_only| データシャッフル前|
| mBART | True | No | parallel | train_peft.sh | raid lora_parallel_only| データシャッフル前 |
| mBART | False | No | bt | train_bt.sh | raid mbart_bt_pre_finetuned | |
| mBART | False |No | parallel | train_parallel_only.sh | raid mbart_parallel_only2 ||
| mBART | True |No | parallel | train_peft_parallel_only.sh | raid mbart_lora_parallel_only ||
| mBART | True | bt_pre | parallel | train_parallel_after_bt.sh | raid mbart_parallel_after_bt | 予想通り過学習 |
| mBART | True | bt_pre | parallel | train_peft_parallel_after_bt.sh | |まだ|
| mT5 | False | No | parallel | train_parallel_only.sh | mt5_parallel_only |testまだ|



### データセット
|データセット名|内容|
|-- | -- |
|bt | RWC+クローリングデータと逆翻訳による擬似翻訳対<br>事前学習に用いる |
|parallel | 英日クローリングして人手で行を揃えた対訳データ |

### モデル
| mBART | facebook/mbart-large-50-one-to-many-mmt |
| mT5 | google/mt5-base |
checkpointのサイズが両方大体7GB