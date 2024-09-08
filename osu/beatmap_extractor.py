"""
Hey James xoxo
I will code the extractor in the following way
You pass in a zip file to all the .osz archives
and it will spit out a zip file of directories of osu maps!!
Love
Tingyi xxxxxx

Important documentation:
Due to how things are passed in with the unzip function, we need to ensure
that the archive being passed in MUST correspond with the list of beatmap
IDs that is also passed in

i.e
we need to pull beatmapID 69 out of mapset1, and beatmapID 420 out of mapset2.
our archive would look like this:

mapset1
mapset2

and our array of IDs must look like this:
[69, 420]
for it to pull beatmapID 69 out of mapset1, and beatmapID 420 out of mapset2.
"""
import os
import re
import zipfile


def unzip(file_path, destination, beatmap_id): # mostly java translated code
    if not os.path.exists(destination):
        os.makedirs(destination)

    extension_pattern = re.compile(r".osu$", re.IGNORECASE)  # Pattern for .osu files
    beatmap_id_pattern = re.compile(beatmap_id, re.IGNORECASE)

    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            for zip_info in zip_ref.infolist():
                file_name = zip_info.filename
                file_content = zip_ref.read(file_name).decode('utf-8', errors='ignore')

                extension_seen = bool(extension_pattern.search(file_name))
                id_seen = bool(beatmap_id_pattern.search(file_content))

                if (extension_seen and id_seen) or (not extension_seen and not id_seen):
                    new_file_path = os.path.join(destination, file_name)
                    print(f"Unzipping to {new_file_path}")

                    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
                    with open(new_file_path, 'w', encoding='utf-8') as new_file:
                        new_file.write(file_content)

    except Exception as e:
        print("Uh oh, something went wrong.")
        print(e)


def process_osz_archive(archive_directory, output_directory, beatmap_id):
    for filename in os.listdir(archive_directory):
        if filename.endswith(".osz"): # Sanity checking in case of gitignores or other stuff
            file_path = os.path.join(archive_directory, filename)
            output_folder = os.path.join(output_directory, os.path.splitext(filename)[0])

            print(f"Processing {file_path}, extracting to {output_folder}")
            unzip(file_path, output_folder, beatmap_id)

# code is still unfinished and broken, please dont use xx

if __name__ == "__main__":
    unzip("./Test/326920 Seiryu - BLUE DRAGON.osz",
          "output/",
          "898575")

