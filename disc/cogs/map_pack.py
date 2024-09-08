import discord
from discord.ext import commands

from config_example import MAP_PACKS_FOLDER
from helper.helper import Tools
from osu.client import OsuClient
from osu.helper import OsuTools

import uuid


class MapPack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="pack",
        description="Zips beatmap urls together"
    )
    async def pack(self, ctx: commands.Context, *map_urls):
        beatmap_ids = [OsuTools.extract_beatmapset_id_from_url(map_url) for map_url in map_urls]
        osz_files = await OsuClient.osz_files_from_beatmapset_ids(beatmap_ids)

        map_pack_file = MAP_PACKS_FOLDER.joinpath(f"{uuid.uuid4()}.zip")
        Tools.zip_files(osz_files, to_file=map_pack_file)
        
        await ctx.reply(file=discord.File(map_pack_file))


async def setup(bot):
    await bot.add_cog(MapPack(bot))
