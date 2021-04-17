# MorningKizunaAI

キズナアイのおはようツイートがツイートされた際に、通知を送るBOTです。
現在、Slack BotとDiscord Botに対応しています。
Google fromにwebhookURLを送信すると通知が届くようになります。

- グーグルフォーム
https://docs.google.com/forms/d/e/1FAIpQLScrBF_1cD_vNB3E18jl-2FWkd8REe6OMfvs5YeIG_DsQ6vcyg/viewform

webhookURLの取得方法

- Slack: https://slack.com/intl/ja-jp/help/articles/115005265063-Slack-での-Incoming-Webhook-の利用
- Discord:https://discord.com/developers/applications からNew Applicationを押して選択をすると取得できます。

2021年4月28日に行われたLT会で紹介したアプリケーションです。

# How To Use
config.pyを記述する（TwitterAPIのアクセストークンやスプレットシートについての情報が必要です）
また、GCPからSheetsAPIを利用するためのサービスアカウント情報を含んだjsonファイルをディレクトリにおく必要があります。
詳しくは、後述する [# 環境設定について](https://github.com/kurikinton105/MorningKizunaAI#%E7%92%B0%E5%A2%83%E8%A8%AD%E5%AE%9A%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6) を参照ください。

* 実行

```bash
python MorningKizunaAI.py
```

Heroku Schedulerを利用し、10分ごとに定期実行をしています。詳細は[# 環境設定について](https://github.com/kurikinton105/MorningKizunaAI#%E7%92%B0%E5%A2%83%E8%A8%AD%E5%AE%9A%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)の [## Herokuの設定](https://github.com/kurikinton105/MorningKizunaAI#heroku%E3%81%AE%E8%A8%AD%E5%AE%9A%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6) を参照ください。

* テスト実行

```
python TestAI.py
```

## テスト仕様

* テスト１：探索を行い通知が入るかの確認
Numが0の時に新規ツイートが有った時に通知を入れる

1.テスト用のスプレットシートのNumを0にする
2.テスト用のアカウントでツイートをする
3.MorningKizunaAIをテストモードで実行する
4.Slackに通知が来ることを確認
5.テストの判定を行う

期待する出力
`Success`


* Numが1の時に実行した時に、ツイートではないと判別する

1.テスト用のスプレットシートのNumを1以上にする（確認する）
2.テスト用のアカウントでツイートをする
3.MorningKizunaAIをテストモードで実行する
4.テストの判定を行う

期待する出力
`NoMorningTweet`

* ツイートがない場合に何も行わない

1.MorningKizunaAIをテストモードで実行する
2.テストの判定を行う

期待する出力
`NoTweet`

## Using Technology

- Python
- Heroku Scheduler
- TwiterAPI
- Google From
- Googleスプレットシート（SheetsAPI）



# 環境設定について

## config.pyに書く内容
config.py.bummpyを参照してください

## GCPサービスアカウントについて

SheetsAPIを利用するには、GCPでSheetsAPIを有効にしてサービスアカウントを発行する必要があります。
詳しくは、以下のQiitaを参照ください。
[スプレットシートをデータベースぽく使ってみた | Qiita](https://qiita.com/y_a_m_a/items/b4eeb6079e14ee58d737)

### 設定後のファイル構成

```
.
├── .gitignore
├── MorningKizunaAI.py
├── README.md
├── SheetsAPI
│   └── sheet.py 
├── TestAI.py
├── WebhookAction.py
├── config.py
├── requirements.txt
├── runtime.txt
└── sheetdatabase-287613-5fe9ea38007d.json
```


## ライブラリインストールについて

使用ライブラリは以下のコマンドでインストールすることができます。

```bash
pip install -r requirements.txt
```

## Herokuの設定について

このアプリケーションは、Herokuの無料枠を利用して運用している。実際に動かしているコードはサービスアカウント情報なども含まれるため、プライベートリポジトリ内で管理を行なっている。

1.Herokuへ登録やCLIツールをインストールする。（他記事参照）
2.リポジトリ内でのアプリケーションの作成

```bash
heroku create -m アプリケーション名
```

3.Herokuへデプロイ

```bash
git push heroku main
```

4.Heroku上のタイムゾーンを日本時間にする

```bash
heroku config:add TZ=Asia/Tokyo --app アプリケーション名
```

## スプレットシートの設定

スプレットシートは、

- WebHook
- TweetId
- Num
- Log

の4つのシートを用意する。
また、WebHookシートは、Googleフォームで入力した結果を出力するように設定を行う。

### 各シートの設定方法
- WebHook
![image](https://user-images.githubusercontent.com/51431248/115115516-d37a8200-9fcf-11eb-9ee6-0bfee2641ddc.png)
- TweetId
![image](https://user-images.githubusercontent.com/51431248/115115522-e55c2500-9fcf-11eb-994c-c024c6ea2770.png)
- Num
![image](https://user-images.githubusercontent.com/51431248/115115530-eee58d00-9fcf-11eb-8bbf-6df7c4e8238b.png)
- Log
![image](https://user-images.githubusercontent.com/51431248/115115537-f9a02200-9fcf-11eb-844c-4d3430b813b4.png)


