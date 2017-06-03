import bot

myBot = bot.TwitterBot()
api = myBot.getApi()
cursor =  myBot.getCursor()


friends = []
followers = []
ungratefuls = []

def findThem():
    for friend in cursor(api.friends).items():
        friends.append(friend.screen_name)

    for follower in cursor(api.followers).items():
        followers.append(follower.screen_name)

    for ungrateful in friends:
        if not ungrateful in followers:
            print ungrateful
            ungratefuls.append(ungrateful)


    return ungratefuls