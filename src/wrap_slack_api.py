import slack

slack_token = 'slackのトークンを設定'
client = slack.WebClient(slack_token)


def get_user_list():
    users = client.users_list()
    if users['ok']:
        return users['members']
    else:
        return None


def get_user_detail(userid):
    user = client.users_info(user=userid)
    if user['ok']:
        return user
    else:
        return None
