# MBartによる英日歌詞翻訳
https://github.com/huggingface/transformers/tree/main/examples/pytorch/translation
~~よりコピーしたコードでリポジトリを作成しました。~~

https://github.com/Sonata165/ControllableLyricTranslation/tree/main
を元々利用する予定でしたが、謎のGPUやCPUのメモリが足りなくなる現象が解決できそうにない状況です。

transformers/examples/pytorch/translationの内容を実行したところ上手くいきましたので、内容をこのリポジトリにコピーしました。そのためバージョンが一番最初のリンクの指す最新のものではなくなっています。



## シェルプログラム一覧
sh train_XX.sh　で実行
- train_ro.sh
    -   動作を確認しました
    -   言語：英語（en_XX）→ルーマニア語（ro_RO）
    -   モデル：mbart-large-en-ro
    -   データセット：wmt16（hugging faceより）
    -   output_dir以外は変更なし
- train_ro_50.sh
    -   動作を確認しました
    -   train_roに対しモデルのみ変更
    -   モデル：mbart-large-50-one-to-many-mmt
- train_ja.sh
    -   動作を確認しました
    -   モデル：mbart-large-50-one-to-many-mmt（train_ro_50.shから変更なし）
    -   言語：英語（en_XX）→日本語（ja_XX）
    -   データセット：RWC研究用音楽データベースより日本語曲歌詞80曲分
        -   jsonlineファイルに変換済み
    -   sacrebleuをMeCabでtokenizeするよう変更
        -   日本語対応


## 次にやること
- train_jaを実行した時のeval_bleuが0になっている
    -   生成文の確認
    -   データセットが正しく読めているか確認


## ベースラインとして再現するべきもの
- source: 英語歌詞, target: 日本語歌詞
- syllable数・単語境界が元の英語歌詞と一致するよう、また韻を踏むよう翻訳するモデルの作成
- mbart-large-50-one-to-many-mmtを二段階でfinetuning
    -   単言語データ（日本語歌詞）と逆翻訳のペアをデータセットにfinetuning
    -   対訳データ（両方歌詞）をデータセットにfinetuning
- 二段階のfinetuning ->　パラメータの凍結が必要
- special tokenとして文字数（len）、単語境界（bdr）、一文の最後の韻（rhyme）の追加
- これらのspecial tokenを用いたfinetuning

これを満たした上で、新規性を考えて自分の研究として実装します。


## メモ
- train_jaを回している時点でgpuメモリを13GBを食っている。CUDA out of memoryはこれが原因
    -   gpuが24GBあるものを選ぶ
- 今までのプロジェクト（gitにあげていない方）はlightning_moduleをcpuに移す際にgpuやcpuメモリ不足エラーが出ていた
    -   gpuメモリ不足で回していたが、直接の原因ではなさそう
    -   gpuの容量が足りない→lightning moduleがgpuに載せてるものを無理にcpuに動かそうとする→エラー、の可能性がある？
    -   エラーが出ていたのは毎回２つ目のエポック