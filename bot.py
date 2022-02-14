import discord
from discord.ext import commands
from discord_slash import SlashCommand
from confidential import RUN_ID


client = commands.Bot("~")
slash = SlashCommand(client, sync_commands=True, override_type=True)


@client.event
async def on_ready():
    print("time to dox some kiddos")

client.load_extension('cogs.doxcommands')


client.run(RUN_ID)