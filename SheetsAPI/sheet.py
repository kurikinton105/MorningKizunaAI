# 書き込みを行う
import gspread
import json
import datetime
#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials
import config

def Auth_Sheet(credentials_name,SPREADSHEET_KEY,sheet_name,isTest=False):
    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_name, scope)

    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    if isTest == True:
        SPREADSHEET_KEY = config.SPREADSHEET_TEST_KEY
    else:
        SPREADSHEET_KEY = config.SPREADSHEET_KEY
    #共有設定したスプレッドシートのシート1を開く
    Sheet = gc.open_by_key(SPREADSHEET_KEY).worksheet(sheet_name)
    return Sheet

def addId_getURL(id,isTest=False):
    #2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    #認証情報設定
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(config.SheetAuthKeyName, scope)
    #OAuth2の資格情報を使用してGoogle APIにログインします。
    gc = gspread.authorize(credentials)

    #共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    if isTest == True:
        SPREADSHEET_KEY = config.SPREADSHEET_TEST_KEY
    else:
        SPREADSHEET_KEY = config.SPREADSHEET_KEY
    #共有設定したスプレッドシートのシート1を開く
    TweetId = gc.open_by_key(SPREADSHEET_KEY).worksheet("TweetId")
    TweetId = Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,'TweetId',isTest)
    TweetId.update_cell(1,1,str(id))

    #　URLの取得を行う
    WebHook = gc.open_by_key(SPREADSHEET_KEY).worksheet("WebHook")
    URL_List = WebHook.get_all_values()
    URL =[]
    for i in range(len(URL_List)):
        if i != 0:
            URL.append(URL_List[i][1])
    return URL

def get_info(isTest=False):
    TweetId = Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,'TweetId',isTest)
    #Activityの値を受け取る
    tweetId_Data = TweetId.get_all_values()
    id = tweetId_Data[0][0]
    return id


if __name__ == "__main__":
    Auth = Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Num")
    num :int = Auth.get_all_records()[0]['Num']
    num += 1
    Auth.update_cell(2, 1, num)