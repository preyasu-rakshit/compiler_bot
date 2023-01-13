import praw
import creds

#credentials
client_id = creds.client_id
client_secret = creds.client_secret
user_agent = creds.user_agent
username = creds.username
password = creds.password

#initialising an instance
reddit = praw.Reddit(client_id= client_id, client_secret= client_secret, user_agent= user_agent, username= username, password= password)

subred = reddit.subreddit('shitposting')

top = subred.top(limit= 10, time_filter= 'all')
for i in top:
    print(i.url)

