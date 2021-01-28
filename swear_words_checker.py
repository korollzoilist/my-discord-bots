import discord
from discord.ext import commands
from translate import Translator
from config import *

translator = Translator(to_lang="your language") # you should write language(s) you want

swear_words = [
    'cunt', 'dick', 'fuck', 'duck', 'anal', 'crap', 'shit', 'pussy', 'piss',
    'ass', 'bitch', 'nigga', 'nigger', 'slut', 'whore', 'damn', 'fuk', 'niger'
]
swear_words_foreign_lang = [] # here are the words from swear_words in the language you have chosen 
for i in swear_words:
    translation = translator.translate(i)
    swear_words_foreign_lang.append(translation)

cussing_limit = int(input('Enter the limit of cussing: '))
members = {} # here are members who have ever written cuss words

class MyClient(commands.Bot):

    def __init__(self, command_prefix='$'):
      commands.Bot.__init__(self, command_prefix)

    async def kick(self, user_name: discord.Member, *, reason=None):
        await discord.Member.kick(user_name, reason=reason)

    async def on_ready(self):
        print('The bot is working')

    async def on_message(self, message):
        print(f'{message.author} has just sent a message. Text: {message.content}')
        
        for i in swear_words + swear_words_foreign_lang:
            clear_message = message.content.lower().replace(' ', '') # it changes "h e l l o" into "hello"
            if i in clear_message:
                await message.delete()

                if message.author.name not in (admin + special_members):
                    if message.author.name not in members.keys(): # if the author of the message is not in the members dictionary yet
                        members[message.author.name] = 1 # the bot adds them
                    elif message.author.name in members.keys():
                        members[message.author.name] += 1

                    if members[message.author.name] > cussing_limit: # if the author cussed too much
                        await self.kick(message.author) # the bot kicks them
                        del members[message.author.name] # and deletes their name from the dictionary

    async def on_message_delete(self, message):
        print(f'{message.author} has just deleted its message. Text: {message.content}')
        print(members)

client = MyClient()
client.run(TOKEN)
