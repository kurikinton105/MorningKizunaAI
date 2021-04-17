import unittest
from unittest import TestCase
import datetime
import tweepy

import MorningKizunaAI
import SheetsAPI
import WebhookAction
import config


class MorningKizunaAITest(unittest.TestCase):

    def test_MorningKizunaAI1(self):
        """test method for MorningKizunaAI1
        テスト１：探索を行い通知が入るかの確認
        Numが0の時に新規ツイートが有った時に通知を入れる

        0.時刻を朝に設定する
        1.テスト用のスプレットシートのNumを0にする
        2.テスト用のアカウントで画像付きツイートをする
        3.MorningKizunaAIをテストモードで実行する
        4.Slackに通知が来ることを確認
        5.テストの判定を行う

        期待する出力
        `Success`
        """
        # テスト用アカウントでテストを行う
        twitter_id = config.TwitterIdTest
        isTest = True
        # 時刻を朝に設定する
        time_now = datetime.datetime.now()
        time_morning = datetime.datetime(time_now.year, time_now.month, time_now.day, 6, 15, 30, 2000)
        # 1.テスト用のスプレットシートのNumを0にする
        Auth = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Num",isTest)
        num = 0
        Auth.update_cell(2, 1, num)

        # テスト用アカウントで呟く
        # 取得した各種キーを格納---------------------------------------------
        consumer_key =config.API_key_test
        consumer_secret=config.API_key_secret_test
        access_token=config.Access_token_test
        access_token_secret =config.Access_token_secret_test
        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(f"Test1 at { time_now } \n https://t.co/test")
        # テストの判定
        message = MorningKizunaAI.MorningKizunaAI(twitter_id,time_morning,isTest)
        expected = 'Success'
        print("\n==Test1==")
        print(message)
        self.assertEqual(expected, message)

    def test_MorningKizunaAI2(self):
        """test method for MorningKizunaAI2
        Numが1の時に実行した時に、ツイートではないと判別する

        0.時刻を設定する
        1.テスト用のスプレットシートのNumを1以上にする（確認する）
        2.テスト用のアカウントでツイートをする
        3.MorningKizunaAIをテストモードで実行する
        4.テストの判定を行う

        期待する出力
        `NoMorningTweet`
        """
        # テスト用アカウントでテストを行う
        twitter_id = config.TwitterIdTest
        isTest = True
        # 時刻を朝に設定する
        time_now = datetime.datetime.now()
        time_morning = datetime.datetime(time_now.year, time_now.month, time_now.day, 6, 15, 30, 2000)
        # 1.テスト用のスプレットシートのNumを1にする
        Auth = SheetsAPI.sheet.Auth_Sheet(config.SheetAuthKeyName,config.SPREADSHEET_KEY,"Num",isTest)
        num = 1
        Auth.update_cell(2, 1, num)

        # テスト用アカウントで呟く
        # 取得した各種キーを格納---------------------------------------------
        consumer_key =config.API_key_test
        consumer_secret=config.API_key_secret_test
        access_token=config.Access_token_test
        access_token_secret =config.Access_token_secret_test
        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        api.update_status(f"Test2 at { time_now } \n https://t.co/test")

        # テストの判定
        message = MorningKizunaAI.MorningKizunaAI(twitter_id,time_morning,isTest)
        expected = 'NoMorningTweet'
        print("\n==Test2==")
        print(message)
        self.assertEqual(expected, message)

    def test_MorningKizunaAI3(self):
        """test method for MorningKizunaAI3
        ツイートがない場合に何も行わない

        1.MorningKizunaAIをテストモードで実行する
        2.テストの判定を行う

        期待する出力
        `NoTweet`
        """
        # テスト用アカウントでテストを行う
        twitter_id = config.TwitterIdTest
        isTest = True
        time_now = datetime.datetime.now()
        message = MorningKizunaAI.MorningKizunaAI(twitter_id,time_now,isTest)
        expected = 'NoTweet'
        print("\n==Test3==")
        print(message)
        self.assertEqual(expected, message)


if __name__ == "__main__":
    unittest.main()
