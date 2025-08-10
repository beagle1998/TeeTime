import discord 
import os
import pathlib
import random

dir_path = str(pathlib.Path(__file__).parent.absolute())
s_path=dir_path+"/stickers/"

client = discord.Client()

#America/Los_Angeles    Australia/Sydney    1464793200 time=unix time?

#practice time, la and ny. America/Los_Angeles, America/New_York








@client.event 
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content
    if message.author == client.user:
        return

    if msg.startswith('~hello'):
        await message.channel.send('Hello!')

    if msg.startswith('~help'):
        await message.channel.send('''~hello
        ~help
        ~sh sticker hi sends test
        !ran [type]  ex of types=['angry', 'greetings', 'happy', 'random', 'sad']
        ~ran [random] [type2] ex of type2 ['cute', 'ding_dong', 'embarassed', 'food', 'lurk', 'oops', 'question', 'study']
        ~ran random gets a random sticker from random folder
        ''')

    if msg.startswith('~sh'):
        await message.channel.send(file=discord.File(str(dir_path)+'\\stickers\\43109601.png'))
        
    if msg.startswith('~rh'): #random happy
        #print(str(dir_path)+'\\stickers\\43109601.png')
        locat=s_path+"Happy/"

        ra=random.choice(os.listdir(locat))
        await message.channel.send(file=discord.File(locat+ra))

    if msg.startswith('~ran'): #random something
        m_list=(msg.lower()).split("~ran",1)[1]
        m_list=m_list.split()
        m1=m_list[0]
        cur_path=os.listdir(s_path)
        locat=s_path

        if m1 in cur_path:
            locat=s_path+m1+"/"

        if m1 == "random":
            if len(m_list)>1:
                m2=m_list[1]
                if m2 in os.listdir(locat):
                    locat=locat+m2+"/"
            else:
                locat=locat+"/"+random.choice(os.listdir(locat))+"/"
        ra=random.choice(os.listdir(locat))
        await message.channel.send(file=discord.File(locat+ra))


api_key="E20N9WNT3FMJ"










#os.getevn('TOKEN')












