import asyncio
from pathlib import Path
from typing import List, Optional, Tuple, Any

import aiohttp
from ossapi import OssapiAsync, Beatmapset, Beatmap

import config


class OsuClient:
    ossapi = OssapiAsync(config.OSU_API_CLIENT_ID, config.OSU_API_CLIENT_SECRET)

    @classmethod
    async def osz_file_from_beatmapset_id(cls, beatmapset_id: int, no_video: bool = False) -> Optional[Path]:
        try:
            beatmapset: Beatmapset = await cls.ossapi.beatmapset(beatmapset_id)
        except Exception as e:
            print(f"Failed to fetch beatmap {beatmapset_id}: {e}")
            return None

        no_video_suffix = "n" if no_video else ""
        download_endpoint_url = f"https://catboy.best/d/{beatmapset.id}{no_video_suffix}"

        async with aiohttp.ClientSession() as session:
            async with session.get(download_endpoint_url) as response:
                response_content = await response.read()

        osz_name = f"{beatmapset.id} {beatmapset.artist} - {beatmapset.title}{' [no video]' if no_video else ''}.osz"
        osz_file = config.BEATMAPSETS_FOLDER.joinpath(osz_name)

        with open(osz_file, "wb") as f:
            f.write(response_content)

        return osz_file

    @classmethod
    async def osz_files_from_beatmapset_ids(cls, beatmapset_ids: List[int], no_video: bool = False) -> List[Path]:
        beatmapset_ids = filter(lambda x: x is not None, beatmapset_ids)
        tasks = [cls.osz_file_from_beatmapset_id(beatmapset_id, no_video) for beatmapset_id in beatmapset_ids]

        osz_files = await asyncio.gather(*tasks)

        return osz_files


if __name__ == '__main__':
    # Test code
    beatmap_ids = [2186718, 2193331]
    asyncio.run(OsuClient.osz_files_from_beatmapset_ids(beatmap_ids))
