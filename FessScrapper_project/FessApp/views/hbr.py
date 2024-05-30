from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from rest_framework import status
from datetime import datetime,date
import os
import re
from dotenv import load_dotenv
from django.db import connection
from .Filename_generator import generate_filname
from FessApp.mangodb import db


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
        # Find the div with class "pub-date"
        pub_date_div = soup.find('div', class_='pub-date')
        print('pub_date_div',pub_date_div)

        # Extract the date text from the div
        publication_date = pub_date_div.contents[0].strip()
        print('publication_date',publication_date)
        if not publication_date:
             # Find the <link rel> tag
            # Find the <meta> tag with property "article:published_time"
            pub_date_meta = soup.find('meta', property='article:published_time')
            
            if pub_date_meta and 'content' in pub_date_meta.attrs:
                # Extract the publication date and take only the date part
                publication_datetime = pub_date_meta['content']
                publication_date = publication_datetime.split('T')[0]
                print(publication_date)
            else:
                print("Publication date meta tag not found or missing content attribute")
            
        # Find all <p> tags in the webpage
        paragraphs = soup.find_all('p')
        
        # Extract text from <p> tags
        wordings = []
        for paragraph in paragraphs:
            wordings.append(paragraph.get_text())
        
        # Combine the wordings into a single string
        text = '\n'.join(wordings)
        
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
            print("Publication Date:", publication_date)
        else:
            print("Publication Date not found")
    else:
        print("Failed to fetch the webpage:", response.status_code)
    return publication_date, title, text, full_path


# @api_view(['GET','POST'])
def Fess_hbr_Post(request):
    """
    List all instances of MyModel.
    """
    if request.method == 'POST':
        collection_name = request.data.get("collectionName")
        link = request.data.get("link")
        publication_date, title, text , full_path= Fetch_Content(link,collection_name)
        if publication_date:
            try:
                # Try parsing the date string using the format '%d %B %Y'
                publication_date = datetime.strptime(publication_date, '%b %d, %Y').date().isoformat()
            except ValueError:
                try:
                    # If parsing using '%d %B %Y' fails, try parsing using '%Y-%m-%d'
                    publication_date = datetime.strptime(publication_date, "%Y-%m-%d").date().isoformat()
                except ValueError:
                    return Response("Failed to parse publication date", status=status.HTTP_400_BAD_REQUEST)

        if publication_date and title and text:
            try:
                hrb_rec ={'article_link':link,
                    'article_title':title, 
                    'article_publish_date':publication_date,
                        'article_file_path':full_path}
                    # Access collection of the database 
                mycollection=db[collection_name]
                hbr_rec = mycollection.insert_one(hrb_rec) 

                return full_path
          
            except Exception as e:
                return Response(f"Failed to save data: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                if connection is not None and not connection.is_usable():
                    connection.close()

        else:
            return Response("Failed to fetch content from the provided link", status=status.HTTP_400_BAD_REQUEST)
        
        
  

    

