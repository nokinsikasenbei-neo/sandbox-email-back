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

<img width="1425" alt="スクリーンショット 2022-09-21 18 02 37" src="https://user-images.githubusercontent.com/41631269/191462854-81079348-fbeb-403f-b5ed-4f2a7fb4775d.png">