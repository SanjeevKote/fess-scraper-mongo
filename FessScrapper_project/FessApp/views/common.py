from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from FessApp.mangodb import db
from .guardian import Fess_Gardian_Post
from .Deloitte import Fess_Deloitte_Post
from .sodalitas import Fess_Sodalitas_Post
from .hbr import Fess_hbr_Post
from .economist import Fess_economist_Post
from django.views.decorators.csrf import csrf_exempt
from .docker_copy import docker_copy_from_container
import os

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
        collection_name = request.data.get("collectionName", "").lower()  # Convert to lowercase for case-insensitive comparison
        link = request.data.get("link")
        if 'guardian' in collection_name:
            full_path=Fess_Gardian_Post(request)
        elif 'deloitte' in collection_name:
            full_path=Fess_Deloitte_Post(request)
        elif 'sodalitas' in collection_name:
            full_path=Fess_Sodalitas_Post(request)
        elif 'hbr' in collection_name:
            full_path=Fess_hbr_Post(request)
        elif 'economist' in collection_name:
            full_path=Fess_economist_Post(request)


        docker_copy_from_container("fess-scrapper-api", full_path, os.getenv('SERVER_FILE_PATH'))
        return Response({
                    "message": "Data successfully saved",
                    "file_path": full_path
                }, status=status.HTTP_201_CREATED)