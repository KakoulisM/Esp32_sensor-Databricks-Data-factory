import os
import shutil
from datetime import datetime
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient



TENANT_ID="0464daa0-dcd6-4bc2-9436-4ade7e12b663"
CLIENT_ID="e83b5c90-d72b-4539-bc71-a01380d3b27b"
CLIENT_SECRET="3h.8Q~aWfb4MhqWci.osSS~BqrbcVEVzmMCAsaFW"


LOCAL_LOG_FILE = "/Users/user111/PycharmProjects/PythonProject7/sensor_log.json"

BACKUP_FOLDER = "backups"

STORAGE_ACCOUNT_NAME = "landinglakeiot"
FILESYSTEM_NAME = "demo"
DIRECTORY_NAME = "raw"



def create_backup():
    if not os.path.exists(LOCAL_LOG_FILE):
        print(f"[WARNING] No log file found to back up at '{LOCAL_LOG_FILE}'")
        return None, None

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"data_log_backup_{timestamp}.json"
    backup_path = os.path.join(BACKUP_FOLDER, backup_filename)

    shutil.copy2(LOCAL_LOG_FILE, backup_path)
    print(f"[INFO] Created backup: {backup_path}")
    return backup_path, backup_filename


def upload_to_adls(local_file_path, file_name):
    try:
        credential = ClientSecretCredential(TENANT_ID, CLIENT_ID, CLIENT_SECRET)
        service_client = DataLakeServiceClient(
            account_url=f"https://{STORAGE_ACCOUNT_NAME}.dfs.core.windows.net",
            credential=credential
        )
        filesystem_client = service_client.get_file_system_client(FILESYSTEM_NAME)
        directory_client = filesystem_client.get_directory_client(DIRECTORY_NAME)

        file_client = directory_client.get_file_client(file_name)

        with open(local_file_path, "rb") as f:
            file_contents = f.read()

        file_client.upload_data(file_contents, overwrite=True)
        print(f"[SUCCESS] Uploaded {file_name} to ADLS in {FILESYSTEM_NAME}/{DIRECTORY_NAME}")
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")


if __name__ == "__main__":
    backup_path, backup_name = create_backup()
    if backup_path and backup_name:
        upload_to_adls(backup_path, backup_name)
