import discord
from discord.ext import commands

spammers = {}

special_nicknames = [] # you should add your nickname and nicknames of people who shouldn't be kicked

class NoSpamming(commands.Bot):

	def __init__(self, command_prefix=';'):
		commands.Bot.__init__(self, command_prefix)

	async def kick(self, user_name: discord.Member, *, reason=None):
		await discord.Member.kick(user_name, reason=reason)

	async def on_ready(self):
		print('The bot is working')

	async def on_message(self, message):
		if message.author.name not in special_nicknames:
			if message.author.name not in spammers.keys():
				spammers[message.author.name] = [1, message.content]
			elif message.content != spammers[message.author.name][1]:
				spammers[message.author.name][0] = 1
				spammers[message.author.name][1] = message.content
			else:
				spammers[message.author.name][0] += 1

				if spammers[message.author.name][0] > 10:
					await self.kick(message.author)
					del spammers[message.author.name]
			print(spammers)
			print(message.author.name)

token = 'YOUR TOKEN'

no_spamming = NoSpamming()
no_spamming.run(token)