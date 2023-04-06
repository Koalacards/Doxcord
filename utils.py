import discord
from typing import Optional, Dict
import json


def create_embed(title:str, description:str, color: discord.Color) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    return embed

async def send(
    interaction: discord.Interaction,
    embed: discord.Embed,
    view: Optional[discord.ui.View] = None,
    ephemeral: bool = False,
):
    if view:
        await interaction.response.send_message(
            embed=embed, view=view, ephemeral=ephemeral
        )
    else:
        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

def str2dict(dict_str: str) -> Dict:
    json_compatible = dict_str.replace("'", "\"")
    new_dict = json.loads(json_compatible)
    return new_dict
