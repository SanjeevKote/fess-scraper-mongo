from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from rest_framework import status
from datetime import datetime,date
import re
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


def Fetch_Content(link,collection_name):

    file_name,file_path=generate_filname(link,collection_name)

    os.makedirs(file_path, exist_ok=True)
    # URL of the webpage you want to read
    url=link
    
    # Send a GET request to the URL
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the title of the webpage
        title = soup.title.get_text() if soup.title else "No title found"
        
        # Extract the publication date from <meta> tags
        publication_date = None
        meta_tags = soup.find_all('meta', attrs={'name': 'pub_date'})
        for meta_tag in meta_tags:
            if 'content' in meta_tag.attrs:
                publication_date = meta_tag['content']
                break
        
        # Find all <p> tags in the webpage
        paragraphs = soup.find_all('p')
        
        # Extract text from <p> tags
        wordings = []
        for paragraph in paragraphs:
            wordings.append(paragraph.get_text())
        
        # Combine the wordings into a single string
        text = '\n'.join(wordings)
        # Attempt to find the publication date in various possible formats and locations
        date_patterns = [
            r'\b\d{1,2} [ADFJMNOS]\w* \d{4}\b',  # Example: 10 May 2024
            r'\b\d{4}-\d{2}-\d{2}\b',            # Example: 2024-05-10
            r'\b\d{2}-\d{2}-\d{4}\b',              # DD-MM-YYYY
            r'\b\d{2}/\d{2}/\d{4}\b',              # DD/MM/YYYY
            r'\b\d{2}-\d{2}-\d{2}\b',              # MM-DD-YYYY
            r'\b\d{2}/\d{2}/\d{2}\b',              # MM/DD/YYYY
            r'\b\d{2} [a-zA-Z]{3} \d{4}\b',        # DD MMM YYYY
            r'\b[a-zA-Z]{3} \d{1,2}, \d{4}\b',     # MMM DD, YYYY
            r'\b\d{1,2} [a-zA-Z]{3,} \d{4}\b',     # DD Month YYYY
            r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\b'  # YYYY-MM-DDTHH:MM:SS
        ]
        for pattern in date_patterns:
            date_match = re.search(pattern, response.text)
            if date_match:
                publication_date = date_match.group()
                break
        
        # Save the title, publication date, and text content to a file
        full_path=os.path.join(file_path, file_name + '.txt')
        with open(os.path.join(file_path, file_name + '.txt'), 'w', encoding='utf-8') as f:
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
        logger.error("Failed to fetch the webpage: %s", response.status_code)
    return publication_date, title, text, full_path


# @api_view(['GET','POST'])
def Fess_Gardian_Post(request):
    """
    List all instances of MyModel.
    """
    if request.method == 'POST':
        collection_name = request.data.get("collectionName")
        link = request.data.get("link")
        publication_date, title, text , full_path= Fetch_Content(link,collection_name)
        # Get the current date
        current_date = date.today()
        if publication_date:
            try:
                # Try parsing the date string using the format '%d %B %Y'
                publication_date = datetime.strptime(publication_date, '%d %B %Y').date().isoformat()
            except ValueError:
                try:
                    # If parsing using '%d %B %Y' fails, try parsing using '%Y-%m-%d'
                    publication_date = datetime.strptime(publication_date, "%Y-%m-%d").date().isoformat()
                except ValueError:
                    return Response("Failed to parse publication date", status=status.HTTP_400_BAD_REQUEST)

        if publication_date and title and text:
            corrected_path = full_path.replace("\\", "/")
                # Normalize the path
            full_path = os.path.normpath(corrected_path)
            Gardian_rec ={'article_link':link,
                  'article_title':title, 
                  'article_publish_date':publication_date,
                    'article_file_path':full_path}
                # Access collection of the database 
            mycollection=db[collection_name]
            Gardian_rec = mycollection.insert_one(Gardian_rec) 

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
        
        
  

    

