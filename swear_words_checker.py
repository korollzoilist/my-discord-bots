import discord
from discord.ext import commands
from translate import Translator

translator = Translator(to_lang="ru")

swear_words = [
    'cunt', 'dick', 'fuck', 'duck', 'anal', 'crap', 'shit', 'pussy', 'piss',
    'ass', 'bitch', 'nigga', 'nigger', 'slut', 'whore', 'damn', 'fuk', 'niger'
]
swear_words_ru = []
for i in swear_words:
    translation = translator.translate(i)
    swear_words_ru.append(translation)

the_creator = 'koroll'

members = {}

class MyClient(commands.Bot):

    def __init__(self, command_prefix='$'):
      commands.Bot.__init__(self, command_prefix)

    async def kick(self, user_name: discord.Member, *, reason=None):
        await discord.Member.kick(user_name, reason=reason)

    async def on_ready(self):
        print('The bot is working')

    async def on_message(self, message):
        print(
            f'{message.author} has just sent a message. Text: {message.content}'
        )

        for i in swear_words:
            clear_message = message.content.lower().replace(' ', '')
            if i in clear_message:
                await message.delete()

                if message.author.name not in members.keys():
                    members[message.author.name] = 1
                elif message.author.name in members.keys():
                    members[message.author.name] += 1

                if members[message.author.name] > 5:
                    await self.kick(message.author)
                    del members[message.author.name]
                    pass

        for i in swear_words_ru:
            clear_message = message.content.lower().replace(' ', '')
            if i in clear_message:
                await message.delete()
                if message.author not in members:
                    members[message.author.name] = 1
                else:
                    members[message.author.name] += 1

                if members[message.author.name] > 5:
                    await self.kick(message.author)
                    del members[message.author.name]
                    pass

        if the_creator in members:
            del members[the_creator]

    async def on_message_delete(self, message):
        print(
            f'Welp. {message.author} has just deleted its message. Text: {message.content}'
        )
        print(members)

token = 'YOUR TOKEN'

client = MyClient()
client.run(token)
