import requests, json

def WebhookApp(webhook_url,comment, username,image_URL):
    if "discord" in webhook_url:
        # Discord
        main_content = {
                        'username': username,
                        'avatar_url': image_URL,
                        'content':comment
                    }
        headers = {'Content-Type': 'application/json'}

        response  = requests.post(webhook_url, json.dumps(main_content), headers=headers)
        print(response.status_code)
        return response.status_code
    elif "slack" in webhook_url:
        # Slack
        response = requests.post(webhook_url, data = json.dumps({
        'text': comment,  # 通知内容
        'username': username,  # ユーザー名
        'icon_url': image_URL
        }))
        print(response.status_code)
        return response.status_code
    else:
        return Exception("Not found:Webuook")


if __name__ == "__main__":
    webhook_url  = 'https://discord.com/*****'

    WebhookApp(webhook_url,"Hello Discord!","Morning AI",image_URL="https://pbs.twimg.com/profile_images/1317069927329665025/6brGDZxs_400x400.jpg")

