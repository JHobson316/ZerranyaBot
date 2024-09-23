import discord
import os
from dotenv import load_dotenv
import random
import requests
import json
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import VerticalBarsDrawer

load_dotenv()

def get_cat():
  response = requests.get('https://api.thecatapi.com/v1/images/search?breed_ids=ctif&api_key={}'.format(os.getenv('CAT_KEY')))
  json_data = json.loads(response.text)
  retImg = json_data[0]['url']
  retImg2 = retImg.replace('(','').replace(')','')
  print(retImg2)
  return retImg2

def get_dog():
  response = requests.get('https://api.thedogapi.com/v1/images/search?api_key={}'.format(os.getenv('DOG_KEY')))
  json_data = json.loads(response.text)
  retImg = json_data[0]['url']
  retImg2 = retImg.replace('(','').replace(')','')
  print(retImg2)
  return retImg2

# Facts are a premium feature with the API, so no go for now

# def get_facts():
#    catFacts = 'https://api.thecatapi.com/v1/facts?api_key={}'.format(cKey)
#    dogFacts = 'https://api.thedogapi.com/v1/facts?api_key={}'.format(dKey)
#    snkEyes = random.randint(1,7)
#    print(snkEyes)
#    if snkEyes <=3:
#       reqString = catFacts
#    else:
#       reqString = dogFacts
#    response = requests.get(reqString)
#    print(response)
#    json_data = json.loads(response.text)
#    retString = json_data[0]['fact']
#    print(retString)

def get_bent(link):
   qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
   qr.add_data(link)
   fCode = qr.make_image(image_factory=StyledPilImage, module_drawer=VerticalBarsDrawer())
   fCode.save("qrImage.png")
   return

class MyClient(discord.Client):
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))
  async def on_message(self,message):
    if message.author == self.user:
      return
    elif message.content.startswith('$hello'):
      await message.channel.send('Yooooo!')
    elif message.content.startswith('$roll'):
      luckyRoll = random.randint(1,20)
      if luckyRoll == 20:
        retString = "Your roll is... A NATURAL {}! Awesome!".format(luckyRoll)
        print(retString)
      elif luckyRoll == 1:
        retString = "Your roll is... A NATURAL {}! Less awesome...".format(luckyRoll)
        print(retString)
      else:
        retString = "Your roll is... [{}]".format(luckyRoll)
        print(retString)
      await message.channel.send(retString)
    elif message.content.startswith('$meow'):
            await message.channel.send(get_cat())
    elif message.content.startswith('$bark'):
            await message.channel.send(get_dog())
    elif message.content.startswith('$qr'):
       link = "https://adventofcode.com/2023/day/14"
       get_bent(link)
       await message.channel.send(f'Here you go, {message.author}!')
       await message.channel.send(file=discord.File('qrImage.png'))
       print('Job done :P')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_KEY')) # Replace with your own token.