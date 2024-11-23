import discord

from osu.map import Maps


class MapPackEmbed:
    def __init__(self, maps: Maps, map_pack_url: str = None):  # TODO create MapPack class
        self.maps = maps
        self.map_pack_url = map_pack_url

    def embed(self):

        if self.map_pack_url:
            description = (
f'''[Click the link above to download]
### Maps
{str(self.maps)}''')
            embed = discord.Embed(
                title="Map Pack",
                url=self.map_pack_url,
                description=description,
                color=discord.Color.pink()
            )
        else:
            description = (
f'''### Maps
[Click to attached file to download]
{str(self.maps)}''')
            embed = discord.Embed(
                title="Map Pack",
                description=description,
                color=discord.Color.pink()
            )
        embed.set_author(name="osu!")
        return embed
