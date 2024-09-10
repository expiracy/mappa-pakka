import logging
import re
from typing import Optional

from helper.log import Logger


class BeatmapsetId:
    def __init__(self, beatmapset_id: int, game_mode: str):
        self.beatmapset_id = beatmapset_id
        self.game_mode = game_mode

    def url(self):
        return f"https://osu.ppy.sh/beatmapsets/{self.beatmapset_id}#{self.game_mode}"

    def __repr__(self):
        return str(self)

    def __str__(self):
        url = self.url()

        if url is None:
            return "Invalid OsuUrl"

        return url


class BeatmapId(BeatmapsetId):
    def __init__(self, beatmapset_id: int, game_mode: str, beatmap_id: int):
        super().__init__(beatmapset_id, game_mode)
        self.beatmap_id = beatmap_id

    def url(self):
        return f"https://osu.ppy.sh/beatmapsets/{self.beatmapset_id}#{self.game_mode}/{self.beatmap_id}"


class MapIdFactory:
    @staticmethod
    def from_url(url: str) -> Optional[BeatmapId | BeatmapsetId]:
        pattern = re.compile("https://osu.ppy.sh/beatmapsets/([0-9]+)#([a-z]+)/?([0-9]+)?")
        matches = pattern.match(url)

        try:
            beatmapset_id = matches.group(1)
            assert beatmapset_id is not None
            beatmapset_id = int(beatmapset_id)

            game_mode = matches.group(2)
            assert game_mode is not None

            beatmap_id = matches.group(3)
            if beatmap_id is not None:
                beatmap_id = int(beatmap_id)

        except Exception as e:
            Logger.logger.warning(f"Could not extract map ID from [{url}]: {e}")
            return None

        if beatmap_id is not None:
            return BeatmapId(beatmapset_id, game_mode, beatmap_id)
        else:
            return BeatmapsetId(beatmapset_id, game_mode)
