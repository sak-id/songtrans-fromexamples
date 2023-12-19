# MBartによる英日歌詞翻訳
https://github.com/huggingface/transformers/tree/main/examples/pytorch/translation
~~よりコピーしたコードでリポジトリを作成しました。~~

https://github.com/Sonata165/ControllableLyricTranslation/tree/main
を元々利用する予定でしたが、謎のGPUやCPUのメモリが足りなくなる現象が解決できそうにない状況です。

transformers/examples/pytorch/translationの内容を実行したところ上手くいきましたので、内容をこのリポジトリにコピーしました。そのためバージョンが一番最初のリンクの指す最新のものではなくなっています。


## シェルプログラム
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
    -   次のcommitで試します
    -   モデル：mbart-large-50-one-to-many-mmt（train_ro_50.shから変更なし）
    -   言語：英語（en_XX）→日本語（ja_XX）
    -   データセット：RWC研究用音楽データベースより日本語曲歌詞80曲分
        -   jsonlineファイルに変換済み
    -   sacrebleuをMeCabでtokenizeするよう変更
        -   日本語対応


## ベースラインとして再現するべきもの
- source: 英語歌詞, target: 日本語歌詞
- syllable数・単語境界と一致するよう、また韻を踏むよう翻訳するモデルの作成
- mbart-large-50-one-to-many-mmtをfinetuning
- special tokenとして文字数（len）、単語境界（bdr）、一文の最後の韻（rhyme）の追加
- これらのspecial tokenを用いたfine-tuning

これを満たした上で、新規性を考えて自分の研究として実装します。
