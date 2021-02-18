import discord
import os
import requests #Import API requests
import json    
import random 
from replit import db #Allows us to use replit database

#When you want to you the client side of the bot
client = discord.Client() 

sad_words = ["sad", "depressed", "unhappy", "angry", "misarable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person!"
]

if "responding" not in db.keys():
  db["responding"] = True


# getting the quotes randomly from zenQuote API
# q = quotes, a = author, defined in zenQuote's API
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

# Allow users to update the amount of encouraging messages
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

# Allow users to delete encouraging messages
def delete_encouragemnets(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

# When you logged in says that 'username' has logged in
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

# If the message is from the bot, don't return anything
# If the message starts with $... then responds...
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))
    
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added")

  if msg.startswith("$delete"):
    encouragements = [] #It's empty because if they aren't any encouraging messages it will return empty
    if "encouragements" in db.keys():
      index = int(msg.split("$delete",1)[1]) #We are deleting the place/index of the word, not the word per se.
      delete_encouragemnets(index)
      encouragements = db["encouragements"] 
    await message.channel.send(encouragements)   

# If the user types $lists will see all the lists of user added encouragements
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)   

#In order to turn on and off the bot
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off")
         
#This is the token of the bot, meaning the password to enter inside the bot(here) and change the code
client.run(os.getenv('TOKEN'))

