import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

import db.dbfunc as dbfunc
from fake_profile import profile_choices, update_profile
from utils import create_embed, send
from views import url_view


class ProfileCommands(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @app_commands.command(name="profiles")
    async def profiles(self, interaction: discord.Interaction):
        """Provides a list of all of the fake profiles you have (with your active profile in bold)!"""
        user = interaction.user
        selected_profile = dbfunc.get_selected_profile(user.id)
        profiles = dbfunc.profiles_for_user(user.id)

        title = f"Profiles for user {user.name}"
        color = discord.Color.dark_purple()
        if len(profiles) == 0:
            description = "You don't have any fake profiles yet! Use `dox` or `create-profile` to make one!"
        else:
            selected_bolded = list(
                map(
                    lambda profile: f"**{profile}** (Active)"
                    if profile == selected_profile
                    else profile,
                    profiles,
                )
            )
            description = "\n".join(selected_bolded)

        await send(interaction, create_embed(title, description, color), view=url_view)

    @app_commands.command(name="create-profile")
    @app_commands.describe(profile_name="Name of your new fake profile!")
    async def create_profile(self, interaction: discord.Interaction, profile_name: str):
        """Creates a new profile under a given name and switches your active profile to it."""
        user = interaction.user
        profiles = dbfunc.profiles_for_user(user.id)
        if profile_name in profiles:
            await send(
                interaction,
                create_embed(
                    "Error",
                    f"You already have a profile named `{profile_name}`.",
                    discord.Color.red(),
                ),
                view=url_view,
            )
        else:
            dbfunc.get_profile(user.id, profile_name)
            description = f"You have successfully created fake profile `{profile_name}`! Use `/dox` to view the profile."
            await send(
                interaction,
                create_embed("Success", description, discord.Color.green()),
                view=url_view,
            )

    @app_commands.command(name="switch-profile")
    @app_commands.describe(profile_name="Name of the profile you want to switch to!")
    async def switch_profile(self, interaction: discord.Interaction, profile_name: str):
        """Switch to make the inputted profile name your new active profile!"""
        user = interaction.user
        profiles = dbfunc.profiles_for_user(user.id)
        if profile_name not in profiles:
            description = f"You have no profile named `{profile_name}`. Use `/create-profile` to make a profile with that name, or `/profiles` to view your profiles."
            await send(
                interaction,
                create_embed("Error", description, discord.Color.red()),
                view=url_view,
            )
        else:
            dbfunc.set_selected_profile(user.id, profile_name)
            description = f"Your active profile is now `{profile_name}`! Use `/dox` to view the profile."
            await send(
                interaction,
                create_embed("Success", description, discord.Color.green()),
                view=url_view,
            )

    @app_commands.command(name="delete-profile")
    @app_commands.describe(profile_name="Name of the profile you want delete.")
    async def delete_profile(self, interaction: discord.Interaction, profile_name: str):
        """Delete one of your existing profiles!"""
        user = interaction.user
        selected_profile = dbfunc.get_selected_profile(user.id)
        if selected_profile == profile_name:
            description = "You cannot delete your active profile. Use `switch-profile` to change profiles."
            await send(
                interaction,
                create_embed("Error", description, discord.Color.red()),
                view=url_view,
            )
            return

        profiles = dbfunc.profiles_for_user(user.id)
        if profile_name not in profiles:
            description = f"You have no profile named `{profile_name}`."
            await send(
                interaction,
                create_embed("Error", description, discord.Color.red()),
                view=url_view,
            )
        else:
            dbfunc.delete_profile(user.id, profile_name)
            description = f"`{profile_name}` has been successfully deleted!"
            await send(
                interaction,
                create_embed("Success", description, discord.Color.green()),
                view=url_view,
            )

    @app_commands.command(name="update-profile-data")
    @app_commands.describe(
        option="The data on your dox profile you wish to update (or `All Options` to change all of the data)"
    )
    @app_commands.choices(option=profile_choices())
    async def update_profile_data(
        self, interaction: discord.Interaction, option: Choice[int]
    ):
        """Update a part or all of your active dox profile to get a different fake option!"""
        user = interaction.user
        user_id = user.id

        profile_name = dbfunc.get_selected_profile(user_id)
        profile_name = (
            profile_name if profile_name else f"{user.name}_first_generated_profile"
        )

        current_profile_dict = dbfunc.get_profile(user_id, profile_name)
        updated_profile_dict = update_profile(current_profile_dict, option.name)
        dbfunc.set_profile(user_id, updated_profile_dict, profile_name)

        title = "Success"
        description = f"Option `{option.name}` has been reset in profile `{profile_name}`! Use `/dox` to see it!"
        color = discord.Color.green()

        await send(
            interaction, embed=create_embed(title, description, color), view=url_view
        )


async def setup(client):
    await client.add_cog(ProfileCommands(client))
