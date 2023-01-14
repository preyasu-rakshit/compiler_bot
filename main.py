import praw
import creds
import requests
import logging
from telegram import Update 
from telegram.ext import *

#logging for the py-telegram-bot library
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


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

def update_database(context):
    'context is a dummy variable for the job scheduler'
    
     #initialising an instance
    reddit = praw.Reddit(client_id= client_id, client_secret= client_secret, user_agent= user_agent, username= username, password= password)
    sub = input("Enter the Subreddit you want to scrape: ")
    subred = reddit.subreddit(sub)
    unsorted_posts = subred.top(limit= 10, time_filter='day')
    posts = sort_posts(unsorted_posts)
    download_posts(posts)

#bot commands
def start(update, context):
    user_id = update.effective_chat.id
    msg = '''Hi! I will now brighten up everyday with motivating quotes, wholesome memes, cute cat/dog videos etc ;)'''
    update.message.reply_text(msg)
    
    with open('users.id', 'a+') as f:
        f.write(str(user_id))

def main():
    # updater = Updater("1677058970:AAELb-SlS4Y2jZGfW2NoeAvfnbkcP0W-Tms")
    # dispatcher = updater.dispatcher
    # j = updater.job_queue

    application = Application.builder().token('5938253500:AAG48XzepJzhAxue4jZ796jw3WI7kDSwg6g').build()
    application.add_handler(CommandHandler('start', start))
    application.run_polling()
    application.idle()


if __name__ == "__main__":
    main()