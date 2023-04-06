import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
import db.dbfunc as dbfunc
from utils import send, create_embed
from views import url_view
from fake_profile import profile_options, update_profile, profile_choices

class DoxCommands(commands.Cog):

    def __init__(self, client: commands.Bot) -> None:
            self.client = client
    
    @app_commands.command(name="dox")
    @app_commands.describe(user="User that you want to dox!")
    async def dox(self, interaction: discord.Interaction, user: discord.Member = None):
        """Dox a selected user (or yourself if you leave the user field blank)!"""
        member = user if user is not None else interaction.user
        user_id = member.id
        dox_data = dbfunc.get_profile(user_id)

        title = f"Personal Information for user {member.name}"
        description = ""
        color = discord.Color.orange()
        embed=create_embed(title, description, color)
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        for index, key in enumerate(profile_options()):
            if key == "All Options":
                continue
            inline = False if index % 4 == 0 else True
            data_value = dox_data[key]
            embed.add_field(name=key, value=data_value, inline=inline)

        await send(interaction, embed=embed, view=url_view)
    
    @app_commands.command(name="update-profile-data")
    @app_commands.describe(option="The data on your dox profile you wish to update (or `All Options` to change all of the data)")
    @app_commands.choices(option=profile_choices())
    async def update_profile_data(self, interaction: discord.Interaction, option: Choice[int]):
        """Update a part or all of your personal dox profile to get a different fake option!"""
        print(f"updating {option.name}")
        user_id = interaction.user.id
        current_profile_dict = dbfunc.get_profile(user_id)
        updated_profile_dict = update_profile(current_profile_dict, option.name)
        dbfunc.set_profile(user_id, updated_profile_dict)

        title = "Success!"
        description = f"Option `{option.name}` has been reset for your profile! Use `/dox` to see it!"
        color = discord.Color.green()

        await send(interaction, embed=create_embed(title, description, color), view=url_view)


async def setup(client):
    await client.add_cog(DoxCommands(client))
