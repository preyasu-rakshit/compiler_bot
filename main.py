import praw

#credentials
client_id = 'kSHCtP4MvLjhwjj3P7BFcg'
client_secret = 'Wbqh3cno-jQ4JJhcpv6QR5N07y51jQ'
user_agent = 'preyasu'
username = 'preyasu'
password = 'redpass1234'

#initialising an instance
reddit = praw.Reddit(client_id= client_id, client_secret= client_secret, user_agent= user_agent, username= username, password= password)

subred = reddit.subreddit('shitposting')

top = subred.top(limit= 10, time_filter= 'all')
for i in top:
    print(i.url)

