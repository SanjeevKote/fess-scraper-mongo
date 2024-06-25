from django.shortcuts import render
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from rest_framework import status
import os
import re
from dotenv import load_dotenv
from django.db import connection
from .Filename_generator import generate_filname
from FessApp.mangodb import db
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


def Fetch_Content(link,collection_name, articlePublishedDate):
    converted_date = articlePublishedDate.replace("-", "")
    file_name,file_path=generate_filname(link,collection_name,converted_date)

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
        # publication_date = None
        # meta_tags = soup.find_all('meta', attrs={'name': 'pub_date'})
        # for meta_tag in meta_tags:
        #     if 'content' in meta_tag.attrs:
        #         publication_date = meta_tag['content']
        #         break
        
        # Find all <p> tags in the webpage
        paragraphs = soup.find_all('p')
        
        # Extract text from <p> tags
        wordings = []
        for paragraph in paragraphs:
            wordings.append(paragraph.get_text())
        
        # Combine the wordings into a single string
        text = '\n'.join(wordings)
        # Attempt to find the publication date in various possible formats and locations
        # date_patterns = [
        #     r'\b\d{1,2} [ADFJMNOS]\w* \d{4}\b',  # Example: 10 May 2024
        #     r'\b\d{4}-\d{2}-\d{2}\b',            # Example: 2024-05-10
        #     r'\b\d{2}-\d{2}-\d{4}\b',              # DD-MM-YYYY
        #     r'\b\d{2}/\d{2}/\d{4}\b',              # DD/MM/YYYY
        #     r'\b\d{2}-\d{2}-\d{2}\b',              # MM-DD-YYYY
        #     r'\b\d{2}/\d{2}/\d{2}\b',              # MM/DD/YYYY
        #     r'\b\d{2} [a-zA-Z]{3} \d{4}\b',        # DD MMM YYYY
        #     r'\b[a-zA-Z]{3} \d{1,2}, \d{4}\b',     # MMM DD, YYYY
        #     r'\b\d{1,2} [a-zA-Z]{3,} \d{4}\b',     # DD Month YYYY
        #     r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\b'  # YYYY-MM-DDTHH:MM:SS
        # ]
        # for pattern in date_patterns:
        #     date_match = re.search(pattern, response.text)
        #     if date_match:
        #         publication_date = date_match.group()
        #         break
        
        # Save the title, publication date, and text content to a file
        full_path=os.path.join(file_path, file_name + '.txt')
        with open(os.path.join(file_path, file_name + '.txt'), 'w', encoding='utf-8') as f:
            f.write(f"Title: {title}\n")
            if articlePublishedDate:
                f.write(f"Publication Date: {articlePublishedDate}\n")
            else:
                f.write("Publication Date not found\n")
            f.write("\n" + text)
        if articlePublishedDate:
            logger.info("Publication Date: %s", articlePublishedDate)
        else:
            logger.warning("Publication Date not found")
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
                    'artcle_sourceSite':"The Guardian",
                    'article_link': link,
                    'article_title': title, 
                    'article_publish_date': publication_date,
                    'article_file_path': full_path,
                    'category' : []
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
