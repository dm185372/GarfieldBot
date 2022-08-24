# bot.py
import os
import boto3
import discord
import requests
import logging
import random
from datetime import date
import calendar

#Logging configuration
logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s', level=logging.INFO)

ssm = boto3.client('ssm')

#TOKEN = os.getenv('DISCORD_TOKEN')
#TENOR_TOKEN = os.getenv('TENOR_TOKEN')
GUILD = 'What Are The Odds?!'

discord_token_param = ssm.get_parameter(Name='discord.token', WithDecryption=True)
TOKEN = discord_token_param["Parameter"]["Value"]

tenor_token_param = ssm.get_parameter(Name='tenor.token', WithDecryption=True)
TENOR_TOKEN = tenor_token_param["Parameter"]["Value"]

channel_id = 402916062452252675 #this is the emotional channel
#channel_id = 848560114172690442 #this is the bot-testing channel

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

my_date = date.today()
day_name = calendar.day_name[my_date.weekday()] #i.e. Friday

def tenorgif():
    search_term = "garfield {}".format(day_name)
    lmt = 50
    random_number = random.randint(0, lmt)

    r = requests.get('https://g.tenor.com/v1/search?q={}&key={}&media_filter=gif&content_filter=medium&limit={}'.format(search_term, TENOR_TOKEN, lmt))
    #logging.info('response code: %s', r.status_code)

    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        garfield_gif = r.json()['results'][random_number]['media'][0]['gif']['url']
        return(garfield_gif)
    else:
        garfield_gif = None

def powerful_quote():
    r = requests.get('https://zenquotes.io/api/today')
    logging.info('response code: %s', r.status_code)

    if r.status_code == 200:
        our_quote = r.json()[0]['q']
        our_author = r.json()[0]['a']
        quote_message = '"{}"- {}'.format(our_quote, our_author)
        return(quote_message)
    else:
        quote_message = None

@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    garfield_gif = tenorgif()
    quote = powerful_quote()

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    mentions = [user.mention for user in client.users]
    greeting_list = ['Enjoy your day today.',
                    'Take some time for yourself today.',
                    'Don\'t work too hard',
                    'You\'re the greatest!',
                    'Thinking of you!',
                    'You da best!',
                    'Make sure to eat some lasagna today.',
                    'You have the makings of a Go-Hard.',
                    'Have a great day.',
                    'Have an awesome day.',
                    'Have a wonderful day.',
                    'You\'re a true pogger!',
                    'Poggers',
                    'Pog!',
                    'The word of the day is: lasagna.',
                    'Enjoy!',
                    'Have a nice morning.',
                    'Hope your day is going well.',
                    'It\'s always a pleasure pogging with you.']

    await channel.send('{}'.format(garfield_gif))
    #await channel.send('Happy {} {}! {}'.format(day_name, random.choice(mentions), random.choice(greeting_list)))
    await channel.send('Happy {} {}! Here\'s today\'s inspirational quote: \n> {}'.format(day_name, random.choice(mentions), quote))

    await client.close()

def lambda_handler(event, context):
    client.run(TOKEN)
