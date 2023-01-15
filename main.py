import praw
import creds
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, JobQueue
import random


#credentials
client_id = creds.client_id
client_secret = creds.client_secret
user_agent = creds.user_agent
username = creds.username
password = creds.password

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


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
        print(i.url)


def sort_posts(raw):
    posts = []
    for post in raw:
        if 'i.redd.it' in post.url:
            posts.append(post)

    return posts

def update_posts():
    global posts
    #initialising a praw instance
    reddit = praw.Reddit(client_id= client_id, client_secret= client_secret, user_agent= user_agent, username= username, password= password)
    sub = input("Enter the Subreddit you want to scrape: ")
    subred = reddit.subreddit(sub)
    unsorted_posts = subred.top(limit= 10, time_filter='day')
    posts = sort_posts(unsorted_posts)

async def test(a):
    print('jjj')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(context._chat_id, random.choice(posts).url)


def main():
    # update_posts()
    application = ApplicationBuilder().token('5938253500:AAG48XzepJzhAxue4jZ796jw3WI7kDSwg6g').build()
    application.job_queue.run_repeating(test, 1)
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    

    application.run_polling()
    


if __name__ == "__main__":
    main()  
