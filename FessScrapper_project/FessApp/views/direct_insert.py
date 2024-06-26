from rest_framework.response import Response
import requests
from rest_framework import status
import os
from dotenv import load_dotenv
from django.db import connection
from FessApp.mangodb import db
from .Filename_generator import generate_filname
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


def Fetch_Content(link, collection_name,title, articlePublishedDate,content):
    converted_date = articlePublishedDate.replace("-", "")
    file_name, file_path = generate_filname(link, collection_name, converted_date)

    os.makedirs(file_path, exist_ok=True)
    
    # URL of the webpage you want to read
    url = link
    
    # Send a GET request to the URL
    response = requests.get(url)
    logger.info("Article link: %s", url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        
        # Save the title, publication date, and text content to a file
        full_path = os.path.join(file_path, file_name + '.txt')

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Publication Date: {articlePublishedDate}\n" if articlePublishedDate else "Publication Date not found\n")
            f.write("\n" + content)

    else:
        logger.error("Failed to fetch the webpage: %s", response.status_code)
    
    return articlePublishedDate, title, content, full_path


# @api_view(['GET','POST'])
@csrf_exempt
def Fess_direct_insertView(request):
    """
    List all instances of MyModel.
    """
    if request.method == 'POST':
        collection_name = request.data.get("collectionName")
        link = request.data.get("article_link")
        title=request.data.get("article_title")
        articlePublishedDate = request.data.get("article_publish_date")
        content=request.data.get("article_content")
        source_site=request.data.get("artcle_sourceSite")

        publication_date, title, content, full_path = Fetch_Content(link, collection_name, title, articlePublishedDate,content)
        print('publication_date',publication_date)
        date_object = datetime.strptime(publication_date, "%Y-%m-%d")
        publication_date = date_object.strftime("%d %B %Y")
       
        if publication_date and title and content:
            
            # Normalize the path
            corrected_path = full_path.replace("\\", "/")
            full_path = os.path.normpath(corrected_path)
            logger.info("Article file path: %s", full_path)
            
            Deloitte_rec = {
                'artcle_sourceSite':source_site,
                'article_link': link,
                'article_title': title, 
                'article_publish_date': publication_date,
                'article_file_path': full_path,
                'category' : []
            }
            
            # Access collection of the database 
            mycollection = db['articles']
            Deloitte_rec = mycollection.insert_one(Deloitte_rec) 
            logger.info("%s data saved successfully", collection_name)

            try:
                # fess_model_instance.save()
                return full_path
            
            except Exception as e:
                return Response(f"Failed to save data: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                if connection is not None and not connection.is_usable():
                    connection.close()

        else:
            return Response("Failed to fetch content from the provided link", status=status.HTTP_400_BAD_REQUEST)
