# src4clientapp 

### 設計方針

自然の屋外雰囲気の二酸化炭素濃度レベルは、400ppm程度
約1,000ppmで２０%程度の人が不快感、眠気を感じ、
2000ppmでは大部分の人が不快感、頭痛、めまいや吐き気を発症する。
[https://www.michell-japan.co.jp/blog/blog3_appnote_rot21-01/]()

- [napkin.io](https://www.napkin.io/)から、30分に1度、
  二酸化炭素濃度の平均を取得し、
  - 0~1000ppmなら、正常をアナウンス（環境は正常だよ！、頑張っていこう！）し、
  - 1000~2000ppmなら、心配そうなアナウンスをし（良くない環境だなぁ、大丈夫？疲れてない？）、
  - 2000~なら、警告をだす（すぐに換気してください！）
  というプログラムである。

### 実装の内容

仮想環境(venv)をつかって、実装していたので、以下コマンドを使い、
仮想環境をたてて、requirements.txtをインストールして、実行する必要があります。
```bash
python -m venv venv
python -m pip install -r requirements.txt
```

#### ディレクトリ構成

動作に必要なものは、色付き字のものである。

- <font color="deeppink">img</font>
  CO2 levelに合わせたキャラクタの画像保存ディレクトリ
- <font color="deeppink">setting</font>
　- setting.toml
    main.pyを動かすためのconfigを保持しているファイル
- <font color="deeppink">wav</font>
  CO2 levelあわせたキャラクタの音声保存ディレクトリ
  - 環境は正常だよ！、頑張っていこう！(normal.wav for level1)
  - 良くない環境だなぁ、大丈夫？疲れてない？(risky.wav for level2)
  - すぐに換気してください！(danger.wav for level3)
- app_base.py
- <font color="deeppink">client.py</font>
  napkinからCO2データの平均を取得するためのクラス
- test_client.py
　client.pyのクラスのテストをするためのプログラム
- test_play.py
　wavを再生するためのライブラリをテストするためのプログラム
- <font color="deeppink">main.py</font>
  本命のプログラム

#### main.py

目的は、napkinからCO2の平均データを取得し、
そのデータの値に応じて、
表示画像切り替えと音声再生を行うことによって、
ユーザーにCO2に関する情報を提供するGUIプログラムである。

画像の切り替えは、スレッドを用いて実装している。

main.py内のmonitor_durationの値を変更することによって、
CO2モニタリングの間隔を変更することができる。


#### client.py

使い方としては、
setting/setting.toml内のnapkinに関するパラメータによって、インスタンスを作成し、
napkinにアクセスするためのURLとheaderをインスタンス内で生成、
get_mean関数によって、napkinからCO2の平均値を取得する。

### 検証の内容と結果

- tkinterを利用したGUIが起動できること
- clientクラスを利用して、CO2の平均データを取得できること
- tkinterによって、キャラクターの画像を表示できること
- tkinterによって、キャラクターの画像を切り替えられること
- winsoundによって、wavを再生できること
- tkinterによって、napkinから取得したCO2の平均データを使って場合分けし、<br>
  その場合分け(level1~level3)によって、表示画像とwav再生の切り替えをできること

以上を確認した。
