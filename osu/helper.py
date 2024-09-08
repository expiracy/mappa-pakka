import re


class OsuTools:
    @staticmethod
    def extract_beatmapset_id_from_url(url: str):
        pattern = re.compile("https://osu.ppy.sh/beatmapsets/([0-9]+).*")

        beatmapset_id_str = pattern.match(url)

        try:
            beatmapset_id = int(beatmapset_id_str.group(1))
        except Exception as e:
            print(f"Could not extract beatmapset id from {url}: {e}")
            return None

        return beatmapset_id
