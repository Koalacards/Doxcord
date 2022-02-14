from discord_slash.cog_ext import manage_commands

guild_ids=[752664024910397522]

dox_options = [
    manage_commands.create_option(
        name="user",
        description="User that you want to dox",
        option_type=6,
        required=True
    )
]

