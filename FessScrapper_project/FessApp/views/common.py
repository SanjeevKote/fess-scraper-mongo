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
from .guardian import Fess_Gardian_Post
from .Deloitte import Fess_Deloitte_Post
from .sodalitas import Fess_Sodalitas_Post
from .hbr import Fess_hbr_Post
from .economist import Fess_economist_Post
from django.views.decorators.csrf import csrf_exempt

# Load environment variables from .env file

@api_view(['GET','POST'])
def Fess_split_Post(request):
    """
    List all instances of MyModel.
    """
    full_path=''
    # # Convert DRF Request to Django HttpRequest
    # django_request = request._request
    if request.method == 'POST':
        collection_name = request.data.get("collectionName")
        link = request.data.get("link")
        if collection_name == 'Guardian' or collection_name == 'guardian':
            full_path=Fess_Gardian_Post(request)
        elif collection_name == 'Deloitte' or collection_name == 'deloitte':
            full_path=Fess_Deloitte_Post(request)
        elif collection_name == 'Sodalitas' or collection_name == 'sodalitas':
            full_path=Fess_Sodalitas_Post(request)
        elif collection_name == 'hbr' or collection_name == 'Hbr':
            full_path=Fess_hbr_Post(request)
        elif collection_name == 'economist' or collection_name == 'Economist':
            full_path=Fess_economist_Post(request)
        return Response({
                    "message": "Data successfully saved",
                    "file_path": full_path
                }, status=status.HTTP_201_CREATED)