from urllib.parse import urlparse
from datetime import datetime
import os

def generate_filname(link, collection_name, publication_date):
    parsed_url = urlparse(link)
    path_parts = parsed_url.path.split('/')

    # Get the current date and time
    now = datetime.now()
    # Format it as a string
    timestamp_str = now.strftime("%Y%m%d%H%M%S")

    # Extract the date from the provided publication date
    Date = publication_date
    print(Date)

    # Construct the base file name
    file_name = f"{collection_name}_{timestamp_str}"
    level1 = 'level1'
    level2 = 'level2'

    # Construct the file path
    path = os.getenv('FILE_PATH')
    # if len(path_parts) >= 3:
    file_path = os.path.join(path, f"{collection_name}/{Date}")
    # else:
    #     file_path = os.path.join(path, f"{collection_name}/{level1}/{level2}/{Date}")

    print('path', file_path)

    return file_name, file_path
