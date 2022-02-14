import discord
from discord.ext import commands
from discord_slash.cog_ext import cog_slash
import db.dbfunc as dbfunc
import vars
import utils

class DoxCommands(commands.Cog):
    @cog_slash(name='dox', description='Dox a selected user!',
    guild_ids=vars.guild_ids,
    options=vars.dox_options)
    async def dox(self, ctx, user:discord.Member=None):
        member = user if user is not None else ctx.author
        user_id = member.id
        dox_data = dbfunc.get_attributes(user_id)
        ip = dox_data.get("ip", None)
        address = dox_data.get("address", None)
        phone = dox_data.get("phone", None)
        name = dox_data.get("name", None)

        title = f"Personal Information for user {member.name}"
        description= f"Name: {name}\nAddress: {address}\nPhone Number: {phone}\nIP Address: {ip}"
        color = discord.Color.orange()

        await ctx.send(embed=utils.create_embed(title, description, color))




def setup(bot):
    bot.add_cog(DoxCommands(bot))