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
    def __init__(self, day_of_week, day, month, mention):
        self.dw = day_of_week
        self.d = day
        self.m = month
        self.mention = mention

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
            message = 'Happy {} {}! Here\'s today\'s inspirational quote: \n> {}'.format(self.dw, self.mention, quote_message)
            return(message)
        else:
            message = None
    
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

        message = 'Happy {} {}! {}'.format(self.dw, self.mention, random.choice(greeting_list))
        return(message)

    def national_what_day(self):
        r = requests.get('https://national-api-day.herokuapp.com/api/today')
        logging.info('response code: %s', r.status_code)

        if r.status_code == 200:
            national_day = random.choice(r.json()['holidays'])
            message = 'Happy {} {}! Today is: \n> {}'.format(self.dw, self.mention, national_day)
            return(message)
        else:
            message = None

    def riddle_me_this(self):
        r = requests.get('https://riddles-api.vercel.app/random')
        logging.info('response code: %s', r.status_code)

        if r.status_code == 200:
            riddle = r.json()['riddle']
            answer = r.json()['answer']
            riddle_string = "{}\n||{}||".format(riddle, answer)
            message = 'Happy {} {}! Riddle me this: \n>>> {}'.format(self.dw, self.mention, riddle_string)
            return(message)
        else:
            message = None

    def get(self):
        garf_done = False
        num_list = [0, 1, 2, 3]
        while not garf_done:
            if not num_list:
                logging.error('List is empty - all calls failed. Exiting out.')
                exit(1)
            else:
                todays_choice = random.choice(num_list)

            if todays_choice == 0:
                logging.info('Attempting powerful quote call')
                our_message = self.powerful_quote()
            elif todays_choice == 1:
                logging.info('Attempting greeting call')
                our_message = self.greeting()
            elif todays_choice == 2:
                logging.info('Attempting hoiday call')
                our_message = self.national_what_day()
            else:
                logging.info('Attempting riddle call')
                our_message = self.riddle_me_this()

            if our_message != None:
                return our_message
                garf_done == True  
            else:
                num_list.remove(todays_choice)
                logging.info('That call failed - rerolling')
                 

@client.event
async def on_ready():
    channel = client.get_channel(channel_id)
    my_date = date.today()
    day_name = calendar.day_name[my_date.weekday()] #i.e. Friday
    month = date.today().strftime("%m")
    day = date.today().strftime("%d")

    for guild in client.guilds:
        if guild.name == GUILD:
            break

    mentions = [user.mention for user in client.users if user.bot == False]

    garf = Garf(day_name, day, month, random.choice(mentions))

    todays_message = garf.get()
    await channel.send('{}'.format(garf.tenorgif()))
    await channel.send(todays_message)

    await client.close()

def lambda_handler(event, context):
    client.run(TOKEN)
