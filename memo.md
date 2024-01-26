# 実行したもの

基本raidにしまう
| モデル | Lora | 事前学習済み | データセット | スクリプト | 保存場所 | 備考 |
| ---- |----|----|----|----|---- | ---- |
| mBART | | | | test_pretrained.sh | mbart_no_train_result | 元のモデル|
| mBART | |  | parallel | train_parallel_only.sh | mbart_parallel_only| 過学習 testまだ|
| mBART |  |  | bt | train_bt.sh | raid mbart_bt_pre_finetuned | 事前学習　新しいtestでtest|
| mBART| | True | parallel| train_parallel_after_bt.sh | mbart_parallel_after_bt | gpu01でtrain中| 
| mBART| True| True | parallel| train_peft_parallel_after_bt.sh | mbart_peft_parallel_after_bt | testまだ| 
| mT5 |  | | bt | train_bt.sh | mt5_bt_pre_finetuned | 事前学習 新しいtestでtest|
| mT5 | |True |parallel| train_parallel_after_bt.sh | mt5_parallel_after_bt | gpu07でtrain中|
| mT5 |True |True |parallel| train_peft_parallel_after_bt.sh | mt5_peft_parallel_after_bt | gpu07でtrain中|


## shuffle_incorrect内
全ての行をシャッフルしていたせいでbleuが上がった
| モデル | Lora | 事前学習済み | データセット | スクリプト | 保存場所 | 備考 |
| ---- |----|----|----|----|---- | ---- |
| mBART |  |  | 学習なし | test_pretrained.sh | pretrained_model_result | 学習前のtest 4.7664|
| mBART |  |  | parallel | train_parallel_only.sh | mbart_parallel_only | 過学習 test bleu |
| mBART | Lora |  | parallel | train_peft_parallel_only.sh | | test bleu 1.5006|
| mBART |  | bt_pre | parallel|train_parallel_after_bt.sh | mbart_parallel_after_bt3 | 過学習 test bleu 3.5175|
| mBART | Lora | bt_pre | parallel | train_peft_parallel_after_bt.sh | mbart_peft_paralllel_after_bt_r16_alpha16 | test bleu 2.8334|
| mBART | Lora | bt_pre | samesyllable | train_peft_samesyl_after_bt.sh | mbart_peft_samesyl_after_bt | test bleu  4.0758 |
| mT5 |  | bt_pre | parallel | train_parallel_after_bt | mt5_parallel_after_bt | test_bleu 2.75 (540)|
| mT5 | Lora | bt_pre | parallel | train_peft_parallel_after_bt.sh|mt5_peft_parallel_after_bt |test bleu 1.9711|

## ジャンル個人適応用
| モデル | Lora | 事前学習済み | データセット | スクリプト | 保存場所 | 備考 |
| ---- |----|----|----|----|---- | ---- |
| mBART | False | No | crawled | train_crawled.sh | mbart_bt_pre_for_genre | checkpoint50586 best|
->bt_preが使える。使わない

## 今使ってない奴ら(unused_for_now内)
| モデル | Lora | 事前学習済み | データセット | スクリプト | 保存場所 | 備考 |
| ---- |----|----|----|----|---- | ---- |
| mBART | False | No | ~~parallel~~ | train_ja.sh |raid_elmo mbart_parallel_only| データシャッフル前|
| mBART | True | No | ~~parallel~~ | train_peft.sh | raid lora_parallel_only| データシャッフル前 |
| mBART | False |No | parallel | train_parallel_only.sh | raid mbart_parallel_only2 ||
| mBART | True |No | ~~parallel~~ | train_peft_parallel_only.sh | raid mbart_lora_parallel_only |データセットに古いものを指定|
| mBART | True |No | parallel | train_peft_parallel_only.sh | raid mbart_lora_parallel_only2 |　新しくした testまだ|
| mBART | True | bt_pre | parallel | train_parallel_after_bt.sh | raid mbart_parallel_after_bt | 予想通り過学習 |
| mBART | True | bt_pre | ~~parallel~~ | train_peft_parallel_after_bt.sh | mbart_peft_parallel_after_bt| r=4　性能あまり　データセット違う |
| mBART | True | bt_pre | parallel | train_peft_parallel_after_bt.sh | mbart_peft_paralllel_after_bt2 | r=8 testまだ|



### データセット
|データセット名|内容|
|-- | -- |
|bt | RWC+クローリングデータと逆翻訳による擬似翻訳対<br>事前学習に用いる |
|parallel | 英日クローリングして人手で行を揃えた対訳データ |
|samesyl | parallelのうち、英日でモーラ数が一致する行のみ抜き出したもの |

### モデル
| mBART | facebook/mbart-large-50-one-to-many-mmt |
| mT5 | google/mt5-base |
checkpointのサイズが両方大体7GB

### 事前学習モデル（逆翻訳でpre-trainingしたもの）
mbart_bt_pre: 
valじゃなくてtestにしてた　valにしてもう一度
|steps | test bleu |
| -- | -- |
| 76014 |2.6671 |
| 50676 | 3.1441|
->50676のままでOK

mt5_bt_pre:
順調にlossが減りbleuが上がっている
最後の三つを検証
|steps | test bleu | eval bleu|
| -- | -- | -- |
|253380 | 4.056 | 16.7 |
|228042 | 4.0442| 16.66| 
|202704 | 3.3694| |
->253380がベスト

mbart_bt_pre_for_genre:
|steps | test bleu |
| -- | -- |
| 75879 | 3.014 |
| 50586 |3.1544 |
->50586がベスト

### peftの学習率、rの決定
mbartのbt-preを使う
epoch 20
|r | alpha | ファイル名 | eval_bleu | test_bleu |
| -- | -- | -- | -- | -- |
| 8 | default(8) | mbart_parallel_after_bt_r8 | 3.0683  |
| 16 | default | mbart_parallel_after_bt_r16 |  3.4881 |
| 16 | 16 | mbart_parallel_after_bt_r16_alpha16 | 5.1639 | 2.8226<br>(1620 step) <br>2.8334<br>(1188 step)|
->r=16, α=16が良さそう