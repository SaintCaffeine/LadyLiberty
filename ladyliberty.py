# ladyliberty.py 
# Instructions: 
# 1. Remeber to add your <TOKEN> at line 95
# 2. Remember to pip install -r requirements.txt    
# ~ err0xc000007b, with ❤️

import discord 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob, Word
import time
import os
import random

PREFIX = ';'
RULES = []

if __name__ == '__main__':
    client = discord.Client()

    async def help(message):
        await message.channel.send(\
f'''**COMMANDS LIST**
-----------------------------------------------------------------------------------------------------
\t1\t|\t{PREFIX}help\t\t show commands list
-----------------------------------------------------------------------------------------------------
\t2\t|\t{PREFIX}rule\t\t return a server rule given the rule number [ `{PREFIX}rule <ruleNumber>` ]
-----------------------------------------------------------------------------------------------------
\t3\t|\t{PREFIX}ds\t\t    detect sentiment on the given statement [ `{PREFIX}ds <statement>` ]
-----------------------------------------------------------------------------------------------------
\t4\t|\t{PREFIX}def\t\t   find definiton of the given word [ `{PREFIX}def <word>` ]
-----------------------------------------------------------------------------------------------------
\t5\t|\t{PREFIX}vote\t\t add democracy to your statement [ `{PREFIX}vote <statement>` ]
-----------------------------------------------------------------------------------------------------
\t6\t|\t{PREFIX}8ball\t\tKnow the certainty. [ `{PREFIX}8ball <statement>` ]
-----------------------------------------------------------------------------------------------------
~ err0xc000007b, with ❤️''')

    async def rules(message):
        try: 
            await message.channel.send(RULES[int(message.content.split()[1])-1])
        except IndexError:
            await message.channel.send(f'Rule not found. [ `{PREFIX}rules <1..3>` ]')
        except:
            await message.channel.send(f'Invalid Syntax. [ `{PREFIX}rules <ruleNumber>` ]')

    async def detectSentiment(message):
        if message.content.__len__() < 155:
            con = message.content.split()
            if con.__len__() > 1:
                sample = message.content[4:]
                await message.channel.send(f'*analyzing "{sample}" ...*')
                vs = SentimentIntensityAnalyzer().polarity_scores(sample)
                comp = '**Postive** [ based on compound ]' if vs['compound'] > 0 else '**Negative** [ based on compound ]'
                await message.channel.send(f'sentiment detection on *"{sample}"*:\n{comp}\n{vs}')
            else:
                await message.channel.send(f'invalid syntax. [ `{PREFIX}ds this is an example statement` ]')
        else:
            await message.channel.send(f'statement too big. [ limit: 150 chars ]')


    async def define(message):
        con = message.content.split()
        if con.__len__() > 1:
            defi = Word(con[1]).definitions
            if '-a' in con:
                await message.channel.send(f'*{con[1].upper()}*\n{defi}\n{message.author.mention}' if defi else 'Not found!')
            else:
                await message.channel.send(f'*{con[1].upper()}:*\n{defi[0]}\n{message.author.mention}' if defi else 'Not found!')
        else: 
            message.channel.send(f'invalid syntax. [ `{PREFIX}def <word>` ]')

    async def ball8(message):
        await message.channel.send(f"> {message.content}\n\
{random.choice(['yes', 'no', 'dont think so', 'certainly', 'affirmative', 'negative'])}, \
{message.author.mention}")
    
    async def vote(message):
       await message.add_reaction('👍🏻')
       await message.add_reaction('👎🏻')

    @client.event
    async def on_ready():
        print(f'Lady Liberty shines bright, since {time.ctime()}')

    FUNCTIONS = {'rule': rules, 'help': help, 'ds': detectSentiment, 'def': define, 'vote': vote, '8ball': ball8}

    @client.event
    async def on_message(message):
        if message.content.startswith(PREFIX):
            try:
                await FUNCTIONS[message.content.split()[0][1:].lower()](message)
            except:
                pass

    client.run('<TOKEN>')
