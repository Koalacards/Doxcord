import json
from typing import Dict, Optional

import discord


def create_embed(
    title: str, description: str, color: discord.Color, footer: bool = False
) -> discord.Embed:
    embed = discord.Embed(title=title, description=description, color=color)
    if footer:
        embed.set_footer(
            text="ALL of the information Doxcord uses is fake, and for entertainment purposes only."
        )
    return embed


async def send(
    interaction: discord.Interaction,
    embed: discord.Embed,
    view: Optional[discord.ui.View] = None,
    ephemeral: bool = False,
):
    kwargs = {}
    kwargs["embed"] = embed
    kwargs["ephemeral"] = ephemeral
    if view:
        kwargs["view"] = view

    await interaction.response.send_message(**kwargs)


def str2dict(dict_str: str) -> Dict:
    json_compatible = dict_str.replace("'", '"')
    new_dict = json.loads(json_compatible)
    return new_dict
