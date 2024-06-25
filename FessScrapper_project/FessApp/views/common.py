
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from FessApp.views.copy_docker_file import copy_file_from_container
from FessApp.views.move_docker_file import move_file_from_container
from .guardian import Fess_Gardian_Post
from .Deloitte import Fess_Deloitte_Post
from .sodalitas import fess_sodalitas_post
from .hbr import Fess_hbr_Post
from .economist import Fess_economist_Post
from .sharedvalue import Fess_Sharedvalue_Post
from django.views.decorators.csrf import csrf_exempt
import logging

# Set up logging
logger = logging.getLogger(__name__)

@api_view(['GET', 'POST'])
@csrf_exempt  # Be cautious using csrf_exempt in production
def Fess_split_Post(request):
    """
    Handle POST requests to save data and return the file path.
    """
    full_path = ''
    
    if request.method == 'POST':
        logger.info('Received POST request with data: %s', request.data)
        
        collection_name = request.data.get("collectionName", "").lower()
        link = request.data.get("link")
        
        try:
            if 'guardian' in collection_name:
                full_path = Fess_Gardian_Post(request)
            elif 'deloitte' in collection_name:
                full_path = Fess_Deloitte_Post(request)
            elif 'sodalitas' in collection_name:
                full_path = fess_sodalitas_post(request)
            elif 'hbr' in collection_name:
                full_path = Fess_hbr_Post(request)
            elif 'economist' in collection_name:
                full_path = Fess_economist_Post(request)
            elif 'sharedvalue' in collection_name:
                full_path = Fess_Sharedvalue_Post(request)
            else:
                logger.error('Invalid collection name: %s', collection_name)
                return Response({"error": "Invalid collection name"}, status=status.HTTP_400_BAD_REQUEST)
            

# Example usage
# container_id = 'your_container_id'
# source_path = '/path/in/container/file'
# destination_path = '/path/on/host/file'

            # copy_file_from_container("fess-scrapper-api", full_path, "D:/tmp")
            #move_file_from_container("fess-scrapper-api", full_path, "D:/tmp")

            logger.info('Data successfully saved to %s', full_path)
            return Response({
                "message": "Data successfully saved",
                "file_path": full_path
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error('Error processing request: %s', str(e), exc_info=True)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
