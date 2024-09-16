"""
DBX upload test
"""
import dropbox


def upload_to_dropbox(file_from, file_to):
    dbx = dropbox.Dropbox(app_key="",
                          app_secret="",
                          oauth2_access_token="",
                          oauth2_refresh_token="")

    with open(file_from, "rb") as f:
        dbx.files_upload(f.read(), file_to)

    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file_to)

    return shared_link_metadata.url


if __name__ == '__main__':
    file_path = './Test/stinky.zip'
    destination_path = '/mappapakka/stinky.zip'
    url = upload_to_dropbox(file_path, destination_path)
    print(f"Download link: {url}")
