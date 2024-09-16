from pathlib import Path
from typing import Optional

import dropbox
from dropbox.exceptions import ApiError
from dropbox.sharing import CreateSharedLinkWithSettingsError

import config
from helper.log import Logger


class DbxClient:
    dbx_path = "/mappapakka/"

    client = dropbox.Dropbox(
        app_key=config.DROPBOX_APP_KEY,
        app_secret=config.DROPBOX_APP_SECRET,
        oauth2_access_token=config.DROPBOX_ACCESS_TOKEN,
        oauth2_refresh_token=config.DROPBOX_REFRESH_TOKEN
    )

    @classmethod
    def upload_file(cls, path: Path) -> Optional[str]:
        dropbox_file_path = f"{cls.dbx_path}{path.name}"

        with open(path, "rb") as f:
            r = cls.client.files_upload(f.read(), dropbox_file_path)
            Logger.mappa_pakka.info(f"Uploaded {path.name} to Dropbox: {r}")

        shared_link_metadata = DbxClient.client.sharing_create_shared_link_with_settings(dropbox_file_path)
        Logger.mappa_pakka.info(f"Shared link created: {shared_link_metadata.url}")
        return shared_link_metadata.url

    @classmethod
    def delete_files_in_folder(cls, folder_path) -> bool:
        try:
            result = cls.client.files_list_folder(folder_path)
            Logger.mappa_pakka.info(f"Deleting items in folder {folder_path}: {result}")

            for entry in result.entries:
                cls.client.files_delete_v2(entry.path_lower)
                Logger.mappa_pakka.info(f"Deleted item {entry.path_lower}")

            Logger.mappa_pakka.info("All files in the folder have been deleted.")

            return True

        except Exception as e:
            Logger.mappa_pakka.warning(f"Failed to delete dropbox files: {e}")

            return False
