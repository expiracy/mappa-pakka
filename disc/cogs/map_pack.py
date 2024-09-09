import discord
from discord.ext import commands

from osu.map import Maps
from osu.map_id import MapIdFactory


class MapPack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="pack",
        description="Zips beatmap urls together"
    )
    async def pack(self, ctx: commands.Context, *osu_urls: str):
        map_ids = [MapIdFactory.from_url(url) for url in set(osu_urls)]
        maps = await Maps.from_map_ids(map_ids)
        map_pack = maps.zip()

        if map_pack.stat().st_size > 25e6:
            await ctx.reply(f"Map pack is too large to send: {map_pack.stat().st_size} bytes")
        else:
            await ctx.reply(file=discord.File(map_pack))

        map_pack.unlink()


async def setup(bot):
    await bot.add_cog(MapPack(bot))
