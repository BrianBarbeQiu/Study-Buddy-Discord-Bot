from keep_alive import keep_alive
import discord
import os
import requests
import json
import random
from replit import db
from discord.ext import commands

#server_id = 752951134531879075
start = ["Notes:"]
db["cuecards"] = start
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='`',intents=intents)

flip_coin = [
  "it\'s Heads",
  "it\'s Tails",
  "Heads",
  "Tails"
]

cuecards=[]
rnd_add = [
  "```Note Successfully Added!```",
  "```Done!```",
  "```Got it!```"
]

rnd_delete = [
  "```Note Successfully Deleted!```",
  "```Deleted!```",
  "```Gone!```"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_cuecards(cuecards_notes):
  if "cuecards" in db.keys():
    cuecards = db["cuecards"]
    cuecards.append(cuecards_notes)
    db["cuecards"] = cuecards
  else:
    db["cuecards"] = [cuecards_notes]

def delete_cuecard(index):
  cuecards = db["cuecards"]
  if len(cuecards) > index:
    del cuecards[index]
    db["cuecards"] = cuecards


@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.idle, activity=discord.Game('-help'))
  print('We have logged in as {0.user}'.format(client))
  
@client.event
async def on_message(message):
  id = client.get_guild(752951134531879075)
  if message.author == client.user:
    return

  if message.content.startswith('-help'):
    await message.channel.send ("```Study Buddy is a discord bot that helps you with maintaining your notes via discord. It uses databases to help keep track of the data you've stored within it. Created by 53 Bus Gang (Brian Qiu, Edwin Chen, Mohib Khan, Thomas Pazhaidam)\nBelow are the commands for Study Buddy...```")
    await message.channel.send ("```Commands (Prefix \'-\'):\ntype -notes, to access your notes\ntype -new (\"your notes\"), to add new notes to the data base\ntype -del (\"number of note\"), to delete the existing note\ntype -clear, to deleta all the data bases\ntype -flip or -coin, to flip a coin\ntype -motiv, to get a random motivational quote```")

  if message.content.startswith('Thanks Study Buddy'):
    await message.channel.send('```No Problem, Bro```')

  notes = message.content
  options = db["cuecards"]
  
  if notes.startswith("-new"):
    cuecards_notes = notes.split("-new ",1)[1]
    update_cuecards(cuecards_notes)
    if "cuecards" in db.keys():
      options = db["cuecards"]
    await message.channel.send (message.author.mention + random.choice(rnd_add))

  if notes.startswith("-del"):
    if "cuecards" in db.keys():
      index = int(notes.split("-del",1) [1])
      if index != 0:
        delete_cuecard(index)
      await message.channel.send(message.author.mention + random.choice(rnd_delete))
  
  if notes.startswith("-clear"):
    db["cuecards"]= start
    await message.channel.send('```Cleared All Notes```')

  if message.content.startswith('-notes'):
    if "cuecards" in db.keys():
      await message.channel.send('```%s```' % '\n-'.join(map(str, options)))
      
  if message.content.startswith('-flip'):
    await message.channel.send(message.author.mention + " You got..." + "```" + random.choice(flip_coin) + "```")
    emoji = '✅'
    await message.add_reaction(emoji)

  if message.content.startswith('-coin'):
    await message.channel.send(message.author.mention + " You got..." + "```" + random.choice(flip_coin) + "```")
    emoji = '✅'
    await message.add_reaction(emoji)

  if message.content.startswith('-motiv'):
    quote = get_quote()
    await message.channel.send(quote)
    emoji = '✅'
    await message.add_reaction(emoji)
  
  if message.content == "-users":
    await message.channel.send(f"""There are {id.member_count} Members in the server""")

keep_alive() #Up keep
client.run(os.getenv('TOKEN'))

