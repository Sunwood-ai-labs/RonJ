1 名前：AIに詳しい人 2023/03/29(水) 22:55:13.48 ID:ai3141
この論文、ViTARって新しいVision Transformerのアーキテクチャを提案してるみたいやな。任意の解像度の画像に対応できるようにしてるみたいやけど、どんな感じなんやろ？

2 名前：ディープラーニング初心者 2023/03/29(水) 22:57:36.54 ID:dl1234 
Vision Transformerってなんですか？よく聞くTransformerとは違うんですか？

3 名前：コンピュータビジョン研究者 2023/03/29(水) 23:03:01.66 ID:cv9876
＞＞2 Vision Transformerは画像認識のためにTransformerアーキテクチャを利用したモデルのことやな。従来のCNNベースと比べて性能が高いことが知られとるで。
でもな、解像度が学習時と違うと性能が落ちるっていう問題点があったんや。そこをこの研究では解決しようとしてるみたいやな。

4 名前：自然言語処理の専門家 2023/03/29(水) 23:07:43.21 ID:nl7777
Transformerは元々自然言語処理のために開発されたアーキテクチャやからな。それを画像に応用するのはおもしろい発想やと思うで。
位置情報をどうやって組み込むかとかが肝になりそうやな。

5 名前：ディープラーニング初心者 2023/03/29(水) 23:11:58.39 ID:dl1234
なるほど、Transformerを画像に使うんですね！位置情報って具体的にはどういうことですか？

6 名前：コンピュータビジョン研究者 2023/03/29(水) 23:18:22.84 ID:cv9876  
＞＞5 畳み込みニューラルネットワーク(CNN)は局所的な位置関係を捉えるのに長けてるんやけど、Transformerはそれが苦手なんや。だから画像に使う時は何らかの工夫が必要になるんや。
この研究ではFuzzy Positional Encodingって手法を使って、学習時とテスト時で位置情報に柔軟性を持たせることで汎化性能を上げようとしてるみたいやな。

7 名前：機械学習エンジニア 2023/03/29(水) 23:25:16.02 ID:ml4649
Adaptive Token Mergerっていうトークン統合の仕組みも提案されてるみたいやな。これによって計算コストを削減しつつ、任意の解像度に対応できるようになってるらしいで。
高解像度の画像になるほどメリットが大きそうやな。  

8 名前：ディープラーニング初心者 2023/03/29(水) 23:30:43.11 ID:dl1234
トークンってのは何のことですか？あと、統合するとどんなメリットがあるんですか？

9 名前：AIに詳しい人 2023/03/29(水) 23:35:57.35 ID:ai3141
＞＞8 トークンっていうのは入力画像をパッチに分割した各領域のことやな。それを段階的に統合していくことで、高解像度画像でも効率的に処理できるようになるんや。
つまり、解像度が上がっても計算量の増加を最小限に抑えられるってわけや。 

10 名前：画像処理に詳しい人  2023/03/29(水) 23:42:11.68 ID:ip1111
物体検出とかセグメンテーションみたいな高解像度の画像を扱うタスクには特に有効そうやな。
この研究では、そういったタスクでも精度を保ちつつ計算コストを半分ぐらいに削減できてるみたいやで。

11 名前：機械学習エンジニア 2023/03/29(水) 23:47:55.33 ID:ml4649
MAEっていう自己教師あり学習の手法とも相性がいいみたいやな。ViTARをMAEで学習させると、従来のViTより少ない学習データでも高い性能が出せるらしいで。
ラベルなしデータを大量に使った学習に応用できそうやな。

12 名前：ディープラーニング初心者 2023/03/30(木) 00:01:06.84 ID:dl1234 
皆さんの説明でだいぶ理解が深まりました！まとめると、ViTARは解像度の違う画像にも柔軟に対応できる新しいVision Transformerで、計算コストを抑えつつ高精度を実現できるすごい手法ってことですね！
自己教師あり学習への応用も期待できそうですね。もっと勉強して使いこなせるようになりたいです。ありがとうございました！