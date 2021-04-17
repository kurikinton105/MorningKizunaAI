import config
import datetime
import tweepy
import WebhookAction
import SheetsAPI.sheet

def GetUserTweet_data( Account,tweet_id,option_time=10):
    # 取得した各種キーを格納---------------------------------------------
    consumer_key =config.API_key
    consumer_secret=config.API_key_secret
    access_token=config.Access_token
    access_token_secret =config.Access_token_secret
    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    #-------------------------------------------------------------------
    #ツイートを取得
    tweets = api.user_timeline(Account, count=20, page=1)
    BaseURL = f"https://twitter.com/{ Account }/status/"
    tweet_data =[]

    for tweet in tweets:
        if tweet_id < tweet.id:
            print(tweet_id,"<",tweet.id)
            TweetURL = BaseURL+str(tweet.id)
            tweet_text = f"{tweet.text}\n{TweetURL}"
            tweet:dict ={"id":tweet.id , "data":tweet_text}
            tweet_data.append(tweet)
    return tweet_data

def isMorningTweet(tweet,time_now,isTest=False):
    isMorningTweet = False
    #time_now = datetime.datetime.now()
    print(int(time_now.hour))
    # 5時にリセットする！
    if int(time_now.hour)== 5:
        Auth = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Num",isTest)
        Auth.update_cell(2,1,0)
        Log = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Log",isTest)
        Log.append_row([str(time_now.strftime("%Y/%m/%d %H:%M:%S")),f"5時代:0"])
    elif 6 <= int(time_now.hour) and int(time_now.hour) < 12: # 時間での判別
        print("朝時間")
        if tweet['data'].find("https://t.co") != -1 and tweet['data'] not in "RT": # 動画のツイート&RTじゃない
            Auth = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Num",isTest)
            num :int = Auth.get_all_records()[0]['Num']
            print(num)
            # その日の始まりのツイートを取得
            if num == 0:
                isMorningTweet = True
                num += 1
                Auth.update_cell(2, 1, num)
                Log = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Log",isTest)
                Log.append_row([str(time_now.strftime("%Y/%m/%d %H:%M:%S")),f"最初のツイート{num}",True])
            else:
                num += 1
                Auth.update_cell(2, 1, num)
                Log = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Log",isTest)
                Log.append_row([str(time_now.strftime("%Y/%m/%d %H:%M:%S")),f"その日の2個以上:{num}",False])
    return isMorningTweet

def MorningKizunaAI(twitter_id,time_now,isTest):
    username :str ="Morning AI"
    image_URL: str ="https://pbs.twimg.com/profile_images/1317069927329665025/6brGDZxs_400x400.jpg"
    num =int(SheetsAPI.sheet.get_info(isTest))
    # ツイートの取得
    tweet_datas=GetUserTweet_data(twitter_id,num)
    # 5時になったら数値の更新
    if int(time_now.hour)== 5:
        Auth = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Num",isTest)
        Auth.update_cell(2,1,0)
        Log = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Log",isTest)
        Log.append_row([str(time_now.strftime("%Y/%m/%d %H:%M:%S")),f"5時代:0"])
    if tweet_datas != []:
        # num をアップデートする
        id = tweet_datas[0]["id"]
        URLs = SheetsAPI.sheet.addId_getURL(id,isTest)
        # 判定を行う
        if isMorningTweet(tweet_datas[0],time_now,isTest) == True:
            #ログをとる
            Log = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Log",isTest)
            Log.append_row([str(time_now.strftime("%Y/%m/%d %H:%M:%S")),str(tweet_datas),True])
            for webhook_url in URLs:
                try:
                    for data in reversed(tweet_datas):
                        WebhookAction.WebhookApp(webhook_url,data["data"],username,image_URL)
                except:
                    continue
            return "Success"
        else:
            #ログをとる
            Log = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Log",isTest)
            Log.append_row([str(time_now.strftime("%Y/%m/%d %H:%M:%S")),str(tweet_datas),False])
            return "NoMorningTweet"
    else:
        return "NoTweet"

if __name__ == "__main__":
    try:
        twitter_id ="aichan_nel"
        time_now = datetime.datetime.now()
        message=MorningKizunaAI(twitter_id,time_now,isTest=False)
        print("message:",message)

    except:
        import traceback
        traceback.print_exc()