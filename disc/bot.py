from pathlib import Path

import discord
from discord.ext import commands

import config
from helper.log import Logger


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        command_prefix = "="

        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        await self.load_cogs()
        await self.tree.sync()
        Logger.mappa_pakka.info(f"Logged in as {self.user}")

    async def load_cogs(self):
        cogs_folder = Path(__file__).parent.joinpath("cogs")

        for cog_file in cogs_folder.glob("*.py"):
            cog_name = cog_file.name[:-3]
            await self.load_extension(f"disc.cogs.{cog_name}")
            Logger.mappa_pakka.info(f"Loaded cog: {cog_name}")
