import discord
from discord.ext import commands
from confidential import RUN_ID


client = commands.Bot("~")


@client.event
async def on_ready():
    print("time to dox some kiddos")

client.load_extension('cogs.doxcommands')


client.run(RUN_ID)