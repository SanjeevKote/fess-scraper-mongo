from django.shortcuts import render
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from rest_framework import status
import os
from dotenv import load_dotenv
from django.db import connection
from .Filename_generator import generate_filname
from FessApp.mangodb import db
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


def Fetch_Content(link, collection_name, articlePublishedDate):
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
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title of the webpage
        title = soup.title.get_text() if soup.title else "No title found"
        
        # Find all <p> tags in the webpage
        paragraphs = soup.find_all('p')
        
        # Extract text from <p> tags
        wordings = [paragraph.get_text() for paragraph in paragraphs]
        
        # Combine the wordings into a single string
        text = '\n'.join(wordings)
        
        # Save the title, publication date, and text content to a file
        full_path = os.path.join(file_path, file_name + '.txt')
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            f.write(f"Publication Date: {articlePublishedDate}\n" if articlePublishedDate else "Publication Date not found\n")
            f.write("\n" + text)
        
        logger.info("Publication Date: %s", articlePublishedDate if articlePublishedDate else "Not found")
    else:
        logger.error("Failed to fetch the webpage: %s", response.status_code)
    
    return articlePublishedDate, title, text, full_path


# @api_view(['GET','POST'])
@csrf_exempt
def Fess_Gardian_Post(request):
    """
    List all instances of MyModel.
    """
    if request.method == 'POST':
        collection_name = request.data.get("collectionName")
        link = request.data.get("link")
        articlePublishedDate = request.data.get("articlePublishedDate")
        
        publication_date, title, text, full_path = Fetch_Content(link, collection_name, articlePublishedDate)
  
        if publication_date and title and text:
            # Normalize the path
            corrected_path = full_path.replace("\\", "/")
            full_path = os.path.normpath(corrected_path)
            logger.info("Article file path: %s", full_path)
            
            try:
                Gardian_rec = {
                    'artcle_sourceSite':collection_name,
                    'article_link': link,
                    'article_title': title, 
                    'article_publish_date': publication_date,
                    'article_file_path': full_path
                }
                
                # Access collection of the database 
                mycollection = db['articles']
                Gardian_rec = mycollection.insert_one(Gardian_rec) 
                logger.info("%s data saved successfully", collection_name)

                return full_path
            except Exception as e:
                return Response(f"Failed to save data: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                if connection is not None and not connection.is_usable():
                    connection.close()

        else:
            return Response("Failed to fetch content from the provided link", status=status.HTTP_400_BAD_REQUEST)
