import discord
from discord.ext import commands
import db.dbfunc as dbfunc
import vars
import utils
from discord.commands import slash_command, Option


class DoxCommands(commands.Cog):
    @slash_command(name='dox', description='Dox a selected user!',
                   guild_ids=vars.guild_ids)
    async def dox(self, ctx, user: Option(discord.Member, "User that you want to dox") = None):
        member = user if user is not None else ctx.author
        user_id = member.id
        dox_data = dbfunc.get_profile(user_id)

        title = f"Personal Information for user {member.name}"
        description = ""
        for key, value in dox_data.items():
            description += f"**{key}**: {value}\n"
        color = discord.Color.orange()

        await ctx.respond(embed=utils.create_embed(title, description, color))

    @slash_command(name='reset-data', description='Reset the data for a selected user!',
                   guild_ids=vars.guild_ids)
    async def reset_data(self, ctx, user: Option(discord.Member, "User that you want to reset") = None):
        member = user if user is not None else ctx.author
        user_id = member.id

        resettable = dbfunc.get_resettable(user_id)
        if not resettable:
            title = "Cannot reset data"
            description = f"{member.name}'s data is currently not resettable\n" \
                          f"If this is you, then use the /dont-reset-me command to be able to reset yourself"
            color = discord.Color.red()

            await ctx.respond(embed=utils.create_embed(title, description, color))
        else:
            new_profile = utils.get_fake_profile()
            dbfunc.set_profile(user_id, new_profile)

            title = "Data reset successful"
            description = f"Successfully reset data for {member.name}"
            color = discord.Color.green()

            await ctx.respond(embed=utils.create_embed(title, description, color))

    @slash_command(name='dont-reset-me', description='Stops your own profile from being reset',
                       guild_ids=vars.guild_ids)
    async def dont_reset_me(self, ctx):
        member = ctx.author
        user_id = member.id
        old_resettable = dbfunc.get_resettable(user_id)
        # Switch resettable around
        resettable = 0 if old_resettable else 1
        dbfunc.set_resettable(user_id, resettable)

        if resettable:
            title = "Your data is resettable"
            description = f"{member.name}'s data is now resettable again"
            color = discord.Color.green()

            await ctx.respond(embed=utils.create_embed(title, description, color))
        else:
            title = "Your data is not resettable"
            description = f"{member.name}'s data is not resettable anymore"
            color = discord.Color.yellow()

            await ctx.respond(embed=utils.create_embed(title, description, color))


def setup(bot):
    bot.add_cog(DoxCommands(bot))
