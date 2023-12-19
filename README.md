# MBartによる英日歌詞翻訳
https://github.com/huggingface/transformers/tree/main/examples/pytorch/translation
~~よりコピーしたコードでリポジトリを作成しました。~~

https://github.com/Sonata165/ControllableLyricTranslation/tree/main
を元々利用する予定でしたが、GPUやCPUのメモリが足りなくなる状況が解決できそうにありません。

transformers/examples/pytorch/translationの内容を実行したところ上手くいきましたので、内容をこのリポジトリにコピーしました。そのためバージョンが一番最初のリンクの指す最新のものではなくなっています。


## シェルプログラム
- train_ro.sh
    -   動作を確認しました
    -   モデル：mbart-large-en-ro
    -   データセット：wmt16（hugging faceより）
    -   output_dir以外は変更なし
