import praw
import creds
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import random

user_list = []

#credentials - kindly replace these with your own keys to run the bot on your local machine.
client_id = creds.client_id
client_secret = creds.client_secret
user_agent = creds.user_agent
username = creds.username
password = creds.password
token = creds.tele_key

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


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
    posts = []
    subs = ['aww', 'getmotivated', 'eyebleach']
    for sub in subs:
        subred = reddit.subreddit(sub)
        unsorted_posts = subred.top(limit= 50, time_filter='week')
        p = sort_posts(unsorted_posts)
        posts += p


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global user_list
    if str(context._chat_id) not in user_list:
        user_list.append(str(context._chat_id))
        message = 'Hii, I will brighten up your day, one cute pic / motivational quote at a time :). Use /send whenever you need some positivity in your life :)'
        photo = random.choice(posts).url
        await context.bot.send_photo(context._chat_id,photo, message)
    
    else:
        await context.bot.send_message(context._chat_id, 'use /send')

async def send_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = random.choice(posts)
    message = post.title
    photo = post.url
    await context.bot.send_photo(context._chat_id,photo, message)


def main():
    global users
    update_posts()

    application = ApplicationBuilder().token(token).build()
    application.job_queue.run_repeating(update_posts, 60*60*24*7)
    
    start_handler = CommandHandler('start', start)
    send_handler = CommandHandler('send', send_posts)
    application.add_handler(start_handler)
    application.add_handler(send_handler)

    application.run_polling()
    


if __name__ == "__main__":
    main()
