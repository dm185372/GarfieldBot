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

class Garf:
    def __init__(self, day_of_week, day, month):
        self.dw = day_of_week
        self.d = day
        self.m = month

    def tenorgif(self):
        search_term = "garfield {}".format(self.dw)
        lmt = 50
        random_number = random.randint(0, lmt)

        r = requests.get('https://g.tenor.com/v1/search?q={}&key={}&media_filter=gif&content_filter=medium&limit={}'.format(search_term, TENOR_TOKEN, lmt))

        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            garfield_gif = r.json()['results'][random_number]['media'][0]['gif']['url']
            return(garfield_gif)
        else:
            garfield_gif = None

    def powerful_quote(self):
        r = requests.get('https://zenquotes.io/api/today')
        logging.info('response code: %s', r.status_code)

        if r.status_code == 200:
            our_quote = r.json()[0]['q']
            our_author = r.json()[0]['a']
            quote_message = '"{}"- {}'.format(our_quote, our_author)
            return(quote_message)
        else:
            quote_message = None
    
    def our_history(self):
        r = requests.get('https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/events/{}/{}'.format(self.m, self.d))
        logging.info('response code: %s', r.status_code)

        if r.status_code == 200:
            event = random.choice(r.json()['events'])
            event_text = event['text']
            event_link = event['pages'][0]['content_urls']['desktop']['page']
            event = "{} - {}".format(event_text, event_link)
            return(event)
        else:
            event = None

    def greeting(self):
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

        return(random.choice(greeting_list))

    def national_what_day(self):
        r = requests.get('https://national-api-day.herokuapp.com/api/today')
        logging.info('response code: %s', r.status_code)

        if r.status_code == 200:
            national_day = random.choice(r.json()['holidays'])
            return(national_day)
        else:
            national_day = None

@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    my_date = date.today()
    day_name = calendar.day_name[my_date.weekday()] #i.e. Friday
    month = date.today().strftime("%m")
    day = date.today().strftime("%d")

    garf = Garf(day_name, day, month)

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    mentions = [user.mention for user in client.users if user.bot == False]

    await channel.send('{}'.format(garf.tenorgif()))
    todays_choice = random.choice([0, 1, 2, 3])
    if todays_choice == 0:
        await channel.send('Happy {} {}! Here\'s today\'s inspirational quote: \n> {}'.format(day_name, random.choice(mentions), garf.powerful_quote()))
    elif todays_choice == 1:
        await channel.send('Happy {} {}! {}'.format(day_name, random.choice(mentions), garf.greeting()))
    elif todays_choice == 2:
        await channel.send('Happy {} {}! On this day in history: \n> {}'.format(day_name, random.choice(mentions), garf.our_history()))
    else:
        await channel.send('Happy {} {}! Today is: \n> {}'.format(day_name, random.choice(mentions), garf.national_what_day()))

    await client.close()

def lambda_handler(event, context):
    client.run(TOKEN)
