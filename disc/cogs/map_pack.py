import discord
from discord.ext import commands

from dbx.dbx_client import DbxClient
from helper.log import Logger
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
            await ctx.reply("The file(s) you have provided us with is larger than the upload limit for Discord, "
                            "please wait as we upload it to dbx")

            try:
                url = DbxClient.upload_file(map_pack)
                maps.cleanup()
                await ctx.reply(f"Your file resides in this link {url}")

            except Exception as e:
                await ctx.reply(f"Something went wrong: {e}")
        else:
            Logger.mappa_pakka.info("Uploading to discord...")  # mainly for timing checks
            maps.cleanup()  # cleanup maps!
            await ctx.reply(file=discord.File(map_pack))

        Logger.mappa_pakka.info(f"Deleting {map_pack.name}")
        map_pack.unlink()


async def setup(bot):
    await bot.add_cog(MapPack(bot))
