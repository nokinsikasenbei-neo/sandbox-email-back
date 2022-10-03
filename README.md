# Backend 
メールクライアントが通信するバックエンドのAPIサーバ。<br>gmail apiを用いたメールの取得と送信、サンドボックス環境での添付ファイルの展開などを行う。

## 起動方法

```
$ git clone https://github.com/nokinsikasenbei-neo/sandbox-email-back.git
$ cd sandbox-email-back
$ docker-compose up -d --build
```

## 事前準備
### 湯浅のみ
`./app`配下に`credentials.json`を配置する。Google CloudにてデスクトップアプリとしてOAuth2.0 クライアントIDを作成する。

`./app`配下に`token.json`が配置されていなければ、まず以下を実行してトークンを発行する。
```
$ cd sandbox-email-back/app
$ python authorize.py
```

## 接続方法
`http://localhost:8000/docs`でFastAPIが提供するAPIドキュメントに接続できる。

<img width="1440" alt="スクリーンショット 2022-10-03 21 34 04" src="https://user-images.githubusercontent.com/41631269/193577759-fb157368-3d8c-479f-af55-1d4e198d09f0.png">

## API仕様
### メッセージ一覧取得機能
`/messages`をGETする。

<img width="1369" alt="スクリーンショット 2022-10-03 21 59 57" src="https://user-images.githubusercontent.com/41631269/193582655-e0d7ca61-1dcf-4fc2-a004-5637d364cd21.png">

###  特定のメッセージ取得機能
`/message`にメッセージIDをパスパラメータとして付与してGETする。この時にファイルの変換がなされ、変換後のファイル名が返される（ファイル名は現状、英数字しか受け付けない）。また、テキストに含まれていたURLとその怪しさ判定結果が返される。

<img width="1359" alt="スクリーンショット 2022-10-03 22 00 40" src="https://user-images.githubusercontent.com/41631269/193582780-972e11ab-d5d6-45b4-9acb-fabc6d808ea2.png">

### 変換後のファイル取得機能
`/file?name=<filename>`でGETして、変換後のファイルを取得することができる。

<img width="1271" alt="スクリーンショット 2022-10-03 22 04 03" src="https://user-images.githubusercontent.com/41631269/193583395-5606d2b6-3274-4dbb-8200-919e8d6a37b3.png">
