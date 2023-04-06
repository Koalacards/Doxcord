import discord
from discord.ext import commands, tasks
from confidential import RUN_ID

class DoxcordClient(commands.Bot):
    def __init__(self, *, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def setup_hook(self) -> None:
        await client.load_extension("cogs.doxcommands")
        await self.tree.sync()

    async def on_ready(self):
        self.update_presence.start()
        print("ready")

    @tasks.loop(minutes=30)
    async def update_presence(self):
        guild_count = str(len(client.guilds))
        await client.change_presence(
            activity=discord.Game(name=f"doxxing in {guild_count} servers! Press /help")
        )

intents = discord.Intents.default()

client = DoxcordClient(command_prefix='~~~', intents=intents)

client.run(RUN_ID)