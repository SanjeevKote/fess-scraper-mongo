from urllib.parse import urlparse
from datetime import datetime
import os
import logging
logger = logging.getLogger(__name__)
pythonfile_name = os.path.basename(__file__)

def generate_filname(link,collection_name):
    parsed_url = urlparse(link)
    path_parts = parsed_url.path.split('/')
    # Get the current date and time
    now = datetime.now()

    # Format it as a string
    timestamp_str = now.strftime("%Y-%m-%d %H_%M_%S")
    Date=now.strftime("%Y_%m_%d")


    file_name = f"{collection_name}_{path_parts[2]}_{timestamp_str}"

    #Construct file_path
    path = os.getenv('FILE_PATH')
    file_path = os.path.join(path, f"{collection_name}\{path_parts[1]}\{path_parts[2]}\{Date}")
    logger.info("Python Filename:,%s ",pythonfile_name, "Publication Date: %s",file_path)
    print(pythonfile_name,file_path)

    return file_name,file_path