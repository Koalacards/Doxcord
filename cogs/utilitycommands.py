import discord
from discord import app_commands
from discord.ext import commands

from confidential import SUGGESTION_CHANNEL_ID
from utils import create_embed, send
from views import url_view


class UtilityCommands(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="help")
    async def help(self, interaction: discord.Interaction) -> None:
        """Displays the commands to use Doxcord!"""
        title = "Doxcord Help Page"
        description = (
            "Welcome to Doxcord, the bot that allows you to dox your friends and create fake profiles!\n\n"
            "**Note: ALL of the information Doxcord uses is completely fake and is meant for entertainment purposes only.**\n\n"
            "**General Commands**\n\n"
            "**dox**: Allows you to dox a user, or yourself. If someone does not have a fake profile yet one will be created for them.\n\n"
            "**suggest**: Make a suggestion or report a bug directly to the Doxcord devs!\n\n"
            "**help**: Displays this message.\n\n"
            "**Fake Profile Commands**\n\n"
            "**profiles**: Lists off all the profiles you have, showing which one is active (the one that will show up when doxxed).\n\n"
            "**create-profile**: Creates a profile with a given name, and makes the new profile your active profile.\n\n"
            "**switch-profile**: Switches active profiles to a different one that you have.\n\n"
            "**delete-profile**: Deletes one of your fake profiles (this cannot be your active profile).\n\n"
            "**update-profile-data**: Updates a piece of information of your active profile. Can also use option `All` to update the whole profile.\n\n"
            "Happy doxxing!"
        )
        color = discord.Color.dark_orange()
        await send(interaction, create_embed(title, description, color), view=url_view)

    @app_commands.command(name="suggest")
    @app_commands.describe(suggestion="Something to suggest for the Doxcord devs!")
    async def suggest(self, interaction: discord.Interaction, suggestion: str) -> None:
        """Suggest an improvement or report a bug regarding Doxcord!"""
        suggestion_channel = self.client.get_channel(SUGGESTION_CHANNEL_ID)
        await suggestion_channel.send(
            embed=create_embed(
                f"New Suggestion from {interaction.user.name}",
                suggestion,
                discord.Color.dark_orange(),
            )
        )

        await send(
            interaction,
            create_embed(
                "Success!",
                "Your suggestion or report has been sent to the devs, thank you for supporting Doxcord!",
                discord.Color.green(),
            ),
            view=url_view,
            ephemeral=True,
        )


async def setup(client):
    await client.add_cog(UtilityCommands(client))
