# bot.py
import os
import discord
import requests
import logging
import json
import random
from datetime import date
import calendar

#Logging configuration
logging.basicConfig(format='%(levelname)s %(asctime)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv('DISCORD_TOKEN')
TENOR_TOKEN = os.getenv('TENOR_TOKEN')
GUILD = 'What Are The Odds?!'
#channel_id = 402916062452252675
channel_id = 848560114172690442

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

@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    garfield_gif = tenorgif()
    await channel.send('{}'.format(garfield_gif))

    await client.close()

client.run(TOKEN)
#tenorgif()