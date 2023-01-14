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
        ext = i.url.split('.')[-1]
        post = requests.get(i.url)
        print(ext)
        with open(f'fetched_media/{name}.{ext}', 'wb+') as file:
            file.write(post.content)
        name += 1


def sort_posts(raw):
    posts = []
    for post in raw:
        if 'i.redd.it' in post.url:
            posts.append(post)

    return posts

def main():
   
    #initialising an instance
    reddit = praw.Reddit(client_id= client_id, client_secret= client_secret, user_agent= user_agent, username= username, password= password)
    sub = input("Enter the Subreddit you want to scrape: ")
    subred = reddit.subreddit(sub)
    unsorted_posts = subred.top(limit= 10, time_filter='day')
    posts = sort_posts(unsorted_posts)
    download_posts(posts)


if __name__ == "__main__":
    main()