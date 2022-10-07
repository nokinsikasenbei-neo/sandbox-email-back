# セキュアなメールクライアント <img width="120" alt="スクリーンショット 2022-10-06 19 56 09" src="https://user-images.githubusercontent.com/41631269/194553460-77e1ed1c-b370-4597-9de5-a2f3a8b25892.png">
## Overview
近年、メールによるフィッシング攻撃やemotetなどOffice製品を介したマルウェア感染の被害が増加しています。こうした被害の課題として、クリックや実行をして良いかの判断はユーザーに委ねられていることが挙げられます。ユーザーはマルウェアなどの危険なファイルを実行してしまう恐れ、不審なURLを確認せずにクリックしてしまう恐れがあります。このような課題の解決策として、セキュアなメールクライアントを開発しました。このメールクライアントではファイルの無害化を予め行うことで危険なファイルの実行を防止します。また、不審なURLを検出し、強調することで不用心なクリックを防止します。

### 機能1 : 不審なURLの強調表示
<img width="808" alt="スクリーンショット 2022-10-07 21 25 19" src="https://user-images.githubusercontent.com/41631269/194552865-d59e6010-255e-4ade-a7a9-5ac5fea37820.png">

### 機能2 : サンドボックス環境でのファイルの無害化
<img width="784" alt="スクリーンショット 2022-10-07 21 25 30" src="https://user-images.githubusercontent.com/41631269/194552858-d9c35db1-1b94-45dd-8d4e-1f5e5ace1271.png">

## Execution environment(As of Oct.7.2022)
- MacBook Pro(intel, メモリ 16GB)
- docker(v20.10.7)

## Setup
以下に本ツールのインストール方法、起動方法を示します。ツールの使用に際し、参考にしてください。

1. こちらの[ドキュメント](https://support.google.com/workspacemigrate/answer/9222992?hl=ja)を参考に、Google CloudにてOAuthウェブクライアントIDを作成する。ただし、手順11の「アプリケーションの種類」は「デスクトップアプリ」を選択する。また、OAuth同意画面の「テストユーザー」に使用するGoogleアカウントのメールアドレスを登録する。
2. 以下のコマンドを実行し、レポジトリをcloneする。
```
$ git clone https://github.com/nokinsikasenbei-neo/sandbox-email-front.git
$ git clone https://github.com/nokinsikasenbei-neo/sandbox-email-back.git
```
3. 手順1で作成したOAuthウェブクライアントIDの認証情報をJSON形式でダウンロードする。ダウンロードしたファイルを`credentials.json`として`./sandbox-email-back/app`配下に配置する。
4. 以下のコマンドを実行すると、ブラウザでGoogleアカウントでログインするよう求められる。
```
$ cd ./sandbox-email-back/app
$ python ./sandbox-email-back/app/authorize.py
```
ログインが完了すると、`The authentication flow has completed. You may close this window.`と表示される。<br>※ 受信メール件数が少ないアカウントでないと、テストするのが難しい。

5. 以下のコマンドを実行し、フロントエンドサーバを起動する。

```
$ cd ./sandbox-email-front
$ docker-compose up -d --build
```

6. 以下のコマンドを実行し、バックエンドサーバを起動する。
```
$ cd ./sandbox-email-back
$ docker-compose up -d --build
```

7. `http://localhost:3000`にアクセスすると、メールクライアントの画面が表示される。
<img width="1437" alt="スクリーンショット 2022-10-07 20 46 36" src="https://user-images.githubusercontent.com/41631269/194545931-2e1c5b22-2fe9-429d-a11e-ad96b717ed56.png">

## Demo
ツールの実効性を検証するために、以下のデモンストレーションで確認した。
1. HTTPSを使用しているサイトのURLが赤く表示され、HTTPを使用しているサイトのURLが青く表示されるかを検証（フィッシング対策）。
2. 受信したDOCXファイルがPDFファイルに変換されるかを検証（マルウェア対策）。

### Demo1: URLの強調表示
![demo1](https://user-images.githubusercontent.com/41631269/194549142-5ef70108-6aa6-43f2-8e0f-f5ea9789e6db.gif)

### Demo2: ファイルの無害化
![demo2](https://user-images.githubusercontent.com/41631269/194549169-b6b1a1bc-0b41-4f9e-b55d-dc335819a276.gif)

## LICENSE
MIT

## Member
- [tomoyasuzuki](https://github.com/tomoyasuzuki)
- [kyotoor](https://github.com/kyotoor)
- [vgaku](https://github.com/vgaku)
- [melonattacker](https://github.com/melonattacker)
