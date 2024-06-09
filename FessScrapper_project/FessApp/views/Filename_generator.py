from urllib.parse import urlparse
from datetime import datetime
import os

def generate_filname(link,collection_name):
    parsed_url = urlparse(link)
    path_parts = parsed_url.path.split('/')
    # Get the current date and time
    now = datetime.now()

    # Format it as a string
    timestamp_str = now.strftime("%Y-%m-%d %H_%M_%S")
    Date=now.strftime("%Y_%m_%d")


    file_name = f"{collection_name}_{path_parts[1]}_{timestamp_str}"
    level1='level1'
    level2='level2'
    #Construct file_path
    path = os.getenv('FILE_PATH')
    print('path_parts[1]',path_parts[1])
    print('path_parts[2]',path_parts[2])
    if path_parts[1] and path_parts[2]:
        file_path = os.path.join(path, f"{collection_name}/{path_parts[1]}/{path_parts[2]}/{Date}")
    else:
        file_path = os.path.join(path, f"{collection_name}/{level1}/{level2}/{Date}")
    print('path',file_path)

    return file_name,file_path