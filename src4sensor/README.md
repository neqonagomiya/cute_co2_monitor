# src4sensor

### 設計方針

- MQTTを行う際に必要な設定をまとめる
  - 設定ファイル（config.txt）の作成<br>（フォーマットは、```設定パラメータ名＝値```）
  - 設定ファイルから設定情報を読みだすクラスの作成
- SCD41のセンサーデータを取得できるようにする
  - SCD41から、co2濃度・温度・湿度を取得するクラスの作成

### 実装の内容

ディレクトリ構成

```
mpy
│  main.py
│
├─configf
│      config.py
│      config.txt
│
├─sensor
│      co2_sensor.py
│
└─umqtt
        simple.py
```


#### main.py

実際に実行されるファイルです。
この中で、

1. 設定ファイルからのconfigパラメータの読み込み
2. ネットワークへの接続
3. MQTTの設定
4. MQTT Brokerへの接続
5. co2センサへのアクセス・SCD41を扱うインスタンス生成・測定開始コマンドの送信
6. 各データ（CO2濃度・温度・湿度）の取得
7. 各データのjson形式への変換
8. 各データのpublish
9. 次のデータの送信待ち（デフォルトでは60秒間）

という流れで実装しています。

#### config/config.py

micropythonなら動くように、標準ライブラリureを使って
Configクラスを作成しました。
<br>config/config.txtの内容を読み出し、main.pyで利用できるようにしています。


#### config/config.txt

主に、MQTTをする際に必要なconfigを
```パラメータ名＝値```
の形式でまとめています。

#### sensor/co2_sensor.py

SCD41を扱うために、SCD4Xクラスを作成しました。
基本的な機能としては、

- 取得したデータ（CO2濃度・温度・湿度）それぞれを返す関数
- _send_cmd
  - コマンドをi2c経由でSCD41に送る関数
- _read_data
  - SCD41からデータを読み取る関数
- _read_reply
  - SCD41からデータを読み取って、CRC(Cyclic Redundancy Check)を行う関数
- start_periodic_measurement
  - SCD41へ計測開始の命令を送る関数
- stop_periodic_measurement
  - SCD41へ計測停止の命令を送る関数
- _check_buffer_crc
  - SCD41から読み取ったデータに対してCRCを行う関数
- _calc_crc8
  - CRC処理を行う関数

#### umqtt/simple.py

[https://github.com/micropython/micropython-lib/tree/master/micropython/umqtt.simple/umqtt]()

より用いました。

#### <font color="deeppink">注意事項</font>

beebotteにpublishする際には、
configf/config.txt内の
```
publish_flag=False
```
から
```
publish_flag=True
```
にする必要があります。

### 検証の内容と結果

- configの読み込み
  - config.pyを使って、```パラメータ名＝値```のフォーマットで記述された<br>
    config.txtの中身を取得できることを確認
- SCD41のセンサデータ読み込み
  - sensor/co2_sensor内のSCD4Xクラスを利用して、<br>
    SCD4Xのデータ（co2濃度・温度・湿度）を取得できることを確認
- beebotteへのpublish試験
  - beebotte上のDashboardにて可視化を行い、publishできていることを確認
- 耐久試験
  - 17:04-19:28（2023/05/25）の間問題なく、beebotteにpublishできることを確認(やる前は、10分程度経過するとOSError:32が出ていた)

### 未実装項目

- 「仮想環境上で動作させることができれば、ハードウェア上でも問題なく動く」<br>
  という説明を鵜呑みにしているため、ハードウェアでの動作が未確認
