import discord
from discord import app_commands
from discord.ext import commands

import db.dbfunc as dbfunc
from fake_profile import profile_options
from utils import create_embed, send
from views import url_view


class DoxCommands(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="dox")
    @app_commands.describe(user="User that you want to dox!")
    async def dox(self, interaction: discord.Interaction, user: discord.Member = None):
        """Dox a selected user (or yourself if you leave the user field blank)!"""
        member = user if user is not None else interaction.user
        user_id = member.id

        profile_name = dbfunc.get_selected_profile(user_id)
        profile_name = (
            profile_name if profile_name else f"{member.name}_first_generated_profile"
        )

        dox_data = dbfunc.get_profile(user_id, profile_name)

        title = f"Personal Information for user {member.name}"
        description = f"Active profile: **{profile_name}** (Use `/switch-profile` to switch your active profile)"
        color = discord.Color.orange()
        embed = create_embed(title, description, color, footer=True)
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        for key in profile_options():
            if key == "All Options":
                continue
            data_value = dox_data[key]
            embed.add_field(name=key, value=data_value, inline=True)

        await send(interaction, embed=embed, view=url_view)


async def setup(client):
    await client.add_cog(DoxCommands(client))
