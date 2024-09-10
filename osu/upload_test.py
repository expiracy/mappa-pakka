"""
Pretty much just a sanity check to see if im uploading correctly
"""
import dropbox

def upload_to_dropbox(file_from, file_to, access_token):
    dbx = dropbox.Dropbox(access_token)

    with open(file_from, "rb") as f:
        dbx.files_upload(f.read(), file_to)

    shared_link_metadata = dbx.sharing_create_shared_link_with_settings(file_to)
    return shared_link_metadata.url

access_token = ''
file_path = './Test/test.zip'
destination_path = '/mappapakka/test.zip'
url = upload_to_dropbox(file_path, destination_path, access_token)
print(f"Download link: {url}")