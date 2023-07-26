# src4napkin

### 設計方針

- [napkin.io](https://www.napkin.io/)上で、以下の機能を持つサーバーを実装
  - 複数のチャネルに対応
  - RESTまたはMQTTで送信された情報を蓄積 (__napkin_environment_store.py__)
  - RESTの要求を受け付け蓄積した情報を送信 (__napkin_environment_stat.py__)
    - 格納された全データ（"CO2","Humidity", "Temperature"ごと）のグラフを返す
    - 指定された期間の全情報
      - 最新30分
      - 最新1時間
    - 指定された期間の最高値/最低値
      - 最新30分
      - 最新1時間
    - 指定された期間の平均/分散
      - 最新30分
      - 最新1時間

### 実装の内容

#### sensor.py

STM32F767の代わりに、
ある範囲のランダムな値を生成するSrv_sensクラスを作成しました

#### post2napkin.py

Srv_sensクラスを使って、
URL（Ex. https://jaistneqo.npkn.net/environment-store/2310063）
にデータを
Json形式を使って、POSTするためのコード

#### napkin_environment_store.py

napkin上
[](https://jaistneqo.npkn.net/environment-store/2310063)
で実際に動いている処理。

上記URLに、POSTされた、Jsonを受け取り、napkin上のstoreに格納する。

#### napkin_environment_stat.py

napkin上
[](https://jaistneqo.npkn.net/environment-stat/{device_id}/{ways}/{periods}/{data_type})
で実際に動いている処理。

ファイル内には、
以下の関数を実装
- chart（時系列グラフを作成し、ブラウザ上でレンダリングする関数）
- timestamp2JST
  （POSTされたJsonには、時間の情報が追加されているがtimestampであるためそれをJST時間に変換する関数）
- pick_data（所望の範囲・所望の種類のデータをピックアップする関数）

各エンドポイントへアクセスした際の挙動は、
（device_idはすでに、センサデータをJSON形式でPOSTしたデバイスにのみ指定可能（現在は2310063のみアクセス可能）
<br>data_typeでは、"CO2", "Temperature", "Humidity"についてのみ対応している）

- ways=="all"
  - periods=="all"
    - 計測開始から最新までの、所望の種類のデータを時系列グラフで表示する
  - periods=="l30m"
    - 最新30分間の所望の種類のデータを時系列グラフで表示する
  - periods=="1h"
    - 最新1時間の所望の種類のデータを時系列グラフで表示する
- ways=="minmax"
  - periods=="l30m"
    - 最新30分間の所望の種類のデータの最大値・最小値をJSON形式で返す
  - periods=="1h"
    - 最新1時間の所望の種類のデータの最大値・最小値をJSON形式で返す
- ways=="mean"
  - periods=="l30m"
    - 最新30分間の所望の種類のデータの平均・分散をJSON形式で返す
  - periods=="1h"
    - 最新1時間の所望の種類のデータの平均・分散をJSON形式で返す

そして、GETによるアクセスのみ許容しており、
エラーハンドリングも一部（404, 405Error）実装している。


### 検証の内容と結果

各実装において、所望の動作を満たしているか確認した。
特に、napkin_environment_store.pyとnapkin_environment_stat.py
に関しては、
各エンドポイントにアクセスし、
ブラウザ上で、グラフが可視化されるか、
所望の処理結果がJSON形式で返ってくる
ことを
post2napkin.pyと、curlとブラウザを用いたアクセスによって、
確認した。

### 未実装項目

-　"CO2", "Temperature", "Humidity"の全てのデータを一度で、ブラウザ上に可視化する
