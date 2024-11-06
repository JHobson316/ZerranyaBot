import discord
import os
from dotenv import load_dotenv
import random
import requests
import json
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import VerticalBarsDrawer
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer

load_dotenv()

def get_cat():
   response = requests.get('https://api.thecatapi.com/v1/images/search?api_key={}'.format(os.getenv('CAT_KEY')))
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

def get_qr(link):
   qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
   qr.add_data(link)
   fCode = qr.make_image(image_factory=StyledPilImage, back_color=(0, 0, 0), fill_color=(14, 103, 199), module_drawer=GappedSquareModuleDrawer())
   fCode.save("qrImage.png")
   return

def get_educated():
  response = requests.get('https://api.api-ninjas.com/v1/facts', headers={'X-Api-Key':'{}'.format(os.getenv('NINJA_KEY'))})
  print(response)
  factStr = json.loads(response.text)
  moddedFact=factStr[0]['fact']
  print(moddedFact)
  retStatement= "Fun Fact: {}".format(moddedFact)
  return retStatement
 
def get_verified(link):
  response = requests.get('https://api.api-ninjas.com/v1/urllookup?url={}'.format(link), headers={'X-Api-Key':'{}'.format(os.getenv('NINJA_KEY'))})
  resFix = json.loads(response.text)
  print(resFix)
  is_valid = resFix['is_valid']
  isp = resFix['isp']
  country = resFix['country']
  region = resFix['region']
  city = resFix['city']
  timezone = resFix['timezone']
  url = resFix['url']
  print(is_valid)
  cDone = "This is the info I've found at {0}: \n is_valid: {1} \n ISP: {6} \n Country: {2} \n Region: {3} \n City: {4} \n Timezone: {5}".format(url,is_valid,country,region,city,timezone, isp)
  return cDone

def get_punny():
  response = requests.get('https://punapi.rest/api/pun')
  print(response)
  punFix = json.loads(response.text)
  print(punFix)
  return

def get_webby(city):
  response = requests.get('https://api.api-ninjas.com/v1/weather?city={}'.format(city), headers={'X-Api-Key':'{}'.format(os.getenv('NINJA_KEY'))})
  print(response)
  weather = json.loads(response.text)
  print(weather)
  return

def get_phoneNum(number):
  response = requests.get('https://api.api-ninjas.com/v1/validatephone?number={}'.format(number), headers={'X-Api-Key':'{}'.format(os.getenv('NINJA_KEY'))})
  resFix = json.loads(response.text)
  intFormat = resFix['format_international']
  is_valid = resFix['is_valid']
  country = resFix['country']
  location = resFix['location']
  timezones = resFix['timezones']
  retMessage = "This is the info I've found at {0}: \n is_valid: {1} \n Country: {2} \n Location: {3} \n Timezones: {4}".format(intFormat, is_valid, country, location, timezones)
  print(retMessage)
  return retMessage
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

class MyClient(discord.Client):
  async def on_ready(self):
    print('Logged on as {0}!'.format(self.user))
  async def on_message(self,message):
    if message.author == self.user:
      return
    elif message.content.startswith('$hello'):
      await message.channel.send('Hello Darling!')
    elif message.content.startswith('$pat'):
      await message.channel.send('**Wags tail enthusiastically** Arf arf!')
    elif message.content.startswith('$roll'):
      luckyRoll = random.randint(1,20)
      match luckyRoll:
        case 1:
          retString = "Your roll is... A natural {}. Oof...".format(luckyRoll)
          print(retString)
        case 20:
          retString = "Your roll is... A NATURAL {}! Awesome!".format(luckyRoll)
          print(retString)
        case _:
          retString = "Your roll is... [{}]".format(luckyRoll)
          print(retString)
      await message.channel.send(retString)
      # if luckyRoll == 20:
      #   retString = "Your roll is... A NATURAL {}! Awesome!".format(luckyRoll)
      #   print(retString)
      # elif luckyRoll == 1:
      #   retString = "Your roll is... A NATURAL {}! Less awesome...".format(luckyRoll)
      #   print(retString)
      # else:
      #   retString = "Your roll is... [{}]".format(luckyRoll)
      #   print(retString)
      
    elif message.content.startswith('$meow'):
            await message.channel.send(get_cat())
    elif message.content.startswith('$bark'):
            await message.channel.send(get_dog())
    elif message.content.startswith('$qr'):
       print(message.content[4:]) #Link for QR Code
       link = message.content[4:]
       get_qr(link)
       print('Pow')
       await message.channel.send(f'Here you go, {message.author}!')
       await message.channel.send(file=discord.File('qrImage.png'))
       print('Job done :P')
    elif message.content.startswith('$fact'):
       await message.channel.send(get_educated())
    elif message.content.startswith('$pun'):
       await message.channel.send(get_punny())
    elif message.content.startswith('$weather'):
       city = message.content[9:]
       print(city)
       await message.channel.send(get_webby(city))
    elif message.content.startswith('$ver'):
       link = message.content[5:]
       await message.channel.send(get_verified(link))
       print('Verfication Done')
    elif message.content.startswith('$phone'):
      number = message.content[7:]
      print(number)
      await message.channel.send(get_phoneNum(number))
      print('Number done')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_KEY')) # Replace with your own token.