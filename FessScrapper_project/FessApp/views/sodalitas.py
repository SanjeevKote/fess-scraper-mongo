
# Create your views here.
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from rest_framework import status
from datetime import datetime,date
import re
import os
from dotenv import load_dotenv
from .Filename_generator import generate_filname
from django.db import connection
from FessApp.mangodb import db
from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

    
def fetch_content(link, collection_name, publication_date):
    try:
        # Generate file name and path
        file_name, file_path = generate_filname(link, collection_name,publication_date)
        os.makedirs(file_path, exist_ok=True)

        # Send a GET request to the URL
        response = requests.get(link)
        logger.info("Fetching content from: %s", link)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the title of the webpage
            title = soup.title.get_text().strip() if soup.title else "No title found"
            logger.info("Article title: %s", title)

            # Find and extract text from all <p> tags
            paragraphs = soup.find_all('p')
            text = '\n'.join(paragraph.get_text() for paragraph in paragraphs)

            # Save the content to a file
            full_path = os.path.join(file_path, f'{file_name}.txt')
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {title}\n")
                if publication_date:
                    f.write(f"Publication Date: {publication_date}\n")
                else:
                    f.write("Publication Date not found\n")
                f.write("\n" + text)

            if publication_date:
                logger.info("Publication Date: %s", publication_date)
            else:
                logger.warning("Publication Date not found")
        else:
            logger.error("Failed to fetch the webpage, status code: %s", response.status_code)
            return None, None, None, None

        return publication_date, title, text, full_path

    except Exception as e:
        logger.error("An error occurred while fetching content: %s", str(e), exc_info=True)
        return None, None, None, None


# @api_view(['GET','POST'])
def fess_sodalitas_post(request):
    """
    Handle POST request to fetch content from a link and save it to the database.
    """
    if request.method == 'POST':
        collection_name = request.data.get("collectionName")
        link = request.data.get("link")
        publication_date = request.data.get("articlePublishedDate")
        print(publication_date)
        
        if not collection_name or not link:
            return Response({"error": "collectionName and link are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            publication_date, title, text, full_path = fetch_content(link, collection_name, publication_date)
            
            if publication_date and title and text and full_path:
                corrected_path = full_path.replace("\\", "/")
                full_path = os.path.normpath(corrected_path)
                logger.info("Article file path: %s", full_path)
                
                sodalitas_rec = {
                    'article_sourceSite':collection_name,
                    'article_link': link,
                    'article_title': title,
                    'article_publish_date': publication_date,
                    'article_file_path': full_path
                }
                
                mycollection = db['articles']
                mycollection.insert_one(sodalitas_rec)
                logger.info("%s data saved successfully", collection_name)
                
                return full_path
            else:
                return Response({"error": "Failed to fetch content from the provided link"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error("Error saving data: %s", str(e), exc_info=True)
            return Response({"error": "Failed to save data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        finally:
            if connection is not None and not connection.is_usable():
                connection.close()
    else:
        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)