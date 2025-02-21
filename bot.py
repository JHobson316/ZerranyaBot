import discord
import os
from dotenv import load_dotenv
import random
import requests
import urllib.parse
import urllib.request
import json
import qrcode
import wikipediaapi
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import VerticalBarsDrawer
from qrcode.image.styles.moduledrawers.pil import GappedSquareModuleDrawer

load_dotenv()

user_agent = "DiscordBot/1.0 (snoopyjchris@gmail.com) python-wikipediaapi"  # Replace with your contact info

# Initialize Wikipedia API with the user agent
wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)

async def urban_search(message):
    query = message.content[7:]
    if not query:
        await message.channel.send("Please provide a term to look up! Use: `$urban <term>`")
        return

    try:
        # Get the data
        term = urllib.parse.quote(query)
        url = f"https://api.urbandictionary.com/v0/define?term={term}"
        headers = {
            'User-Agent': 'DiscordBot/1.0'
        }
        
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode())
        
        if not data['list']:
            await message.channel.send("No definitions found for that term!")
            return
            
        entry = data['list'][0]
        
        # Create embed
        embed = discord.Embed(
            title=entry['word'],
            url=entry['permalink'],
            color=0x00ff00
        )
        
        # Clean up definition and example
        definition = entry['definition'].replace('[', '').replace(']', '')
        example = entry['example'].replace('[', '').replace(']', '')
        
        # Add fields
        embed.add_field(
          name="Definition", 
            value=definition[:1024] if len(definition) > 1024 else definition, 
            inline=False
        )
        
        if example:
            embed.add_field(
                name="Example", 
                value=example[:1024] if len(example) > 1024 else example, 
                inline=False
            )
        
        embed.add_field(
            name="Rating", 
            value=f"👍 {entry['thumbs_up']} | 👎 {entry['thumbs_down']}", 
            inline=True
        )
        
        embed.set_footer(text=f"Definition by {entry['author']}")
        
        await message.channel.send(embed=embed)
        
    except Exception as e:
        await message.channel.send(f"An error occurred: {str(e)}")
        
def get_wiki(query, sentences=3):
    """Get a Wikipedia summary for the given query"""
    try:
        page = wiki.page(query)
        if not page.exists():
            return "Sorry, I couldn't find any Wikipedia article matching that query."
        # Get the first few sentences of the summary
        summary = page.summary[0:1000]  # Limit to 1000 characters
        #For Codedex submission proof
        print(page.summary[0:100])
        if len(summary) == 1000:
            summary = summary[:summary.rindex('.')] + '...'
        
        return f"**{page.title}**\n{summary}\n\nRead more: {page.fullurl}"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

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

def get_funny():
  response = requests.get('https://api.api-ninjas.com/v1/jokes', headers = {'X-Api-Key': '{}'.format(os.getenv('NINJA_KEY'))})
  print(response)
  punFix = json.loads(response.text)
  print(punFix[0]['joke'])
  return punFix[0]['joke']

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
    
    if not message.content.startswith('$'):
      return

    command = message.content[1:].split()[0].lower()  # Get the command part after '$'
    
    match command:
    
        case 'hello':
            await message.channel.send('Hello Darling!')
        case 'pat':
            await message.channel.send('**Wags tail enthusiastically** Arf arf!')
        case 'roll':
            luckyRoll = random.randint(1,20)
            match luckyRoll:
                case 1:
                    retString = "Your roll is... A natural {}. Oof...".format(luckyRoll)
                case 20:
                    retString = "Your roll is... A NATURAL {}! Awesome!".format(luckyRoll)
                case _:
                    retString = "Your roll is... [{}]".format(luckyRoll)
            print(retString)
            await message.channel.send(retString)
        case 'meow':
            await message.channel.send(get_cat())
        case 'bark':
            await message.channel.send(get_dog())
        case 'qr':
            link = message.content[4:]
            print(f'Link for QR Code: {link}')
            get_qr(link)
            await message.channel.send(f'Here you go, {message.author.mention}!')
            await message.channel.send(file=discord.File('qrImage.png'))
            print('Job done :P')
        case 'fact':
            await message.channel.send(get_educated())
        case 'joke':
            await message.channel.send(get_funny())
        case 'weather':
            city = message.content[9:]
            print(city)
            await message.channel.send(get_webby(city))
        case 'ver':
            link = message.content[5:]
            await message.channel.send(get_verified(link))
            print('Verfication Done')
        case 'phone':
            number = message.content[7:]
            print(number)
            await message.channel.send(get_phoneNum(number))
            print('Number done')
        case 'help':
            await message.channel.send('Here are the commands you can use: \n $hello - Say hello to the bot \n $pat - Pat the bot on the head \n $roll - Roll a 20 sided die \n $meow - Get a random cat picture \n $bark - Get a random dog picture \n $qr - Generate a QR code for a given link \n $fact - Get a random fact \n $pun - Get a random pun \n $weather - Get the weather for a given city \n $ver - Verify a given URL \n $phone - Verify a given phone number \n $wiki - Get a summary of a Wikipedia article \n $urban - Search for a term on Urban Dictionary')
        case 'wiki':
            query = message.content[6:]
            await message.channel.send(get_wiki(query))
        case 'urban':
            await urban_search(message)
    

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('DISCORD_KEY')) # Replace with your own token.