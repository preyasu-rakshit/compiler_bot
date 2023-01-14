import praw
import creds
import requests

#credentials
client_id = creds.client_id
client_secret = creds.client_secret
user_agent = creds.user_agent
username = creds.username
password = creds.password


def download_posts(list_of_posts):
    '''Give list of posts to be downloaded'''
    name = 0
    for i in list_of_posts:
        if 'i.redd.it' in i.url:
            ext = i.url.split('.')[-1]
            post = requests.get(i.url)
            print(ext)
            with open(f'fetched_media/{name}.{ext}', 'wb+') as file:
                file.write(post.content)
            name += 1


def main():
   
    #initialising an instance
    reddit = praw.Reddit(client_id= client_id, client_secret= client_secret, user_agent= user_agent, username= username, password= password)
    sub = input("Enter the Subreddit you want to scrape: ")
    subred = reddit.subreddit(sub)
    hot = subred.top(limit= 10)
    download_posts(hot)


if __name__ == "__main__":
    main()