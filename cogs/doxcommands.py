import discord
from discord.ext import commands
import db.dbfunc as dbfunc
import vars
import utils
from discord.commands import slash_command, Option

class DoxCommands(commands.Cog):
    @slash_command(name='dox', description='Dox a selected user!',
    guild_ids=vars.guild_ids)
    async def dox(self, ctx, user:Option(discord.Member, "User that you want to dox")=None):
        member = user if user is not None else ctx.author
        user_id = member.id
        dox_data = dbfunc.get_profile(user_id)

        title = f"Personal Information for user {member.name}"
        description= ""
        for key, value in dox_data.items(): 
            description+= f"{key}: {value}\n\n"
        color = discord.Color.orange()

        await ctx.respond(embed=utils.create_embed(title, description, color))


def setup(bot):
    bot.add_cog(DoxCommands(bot))