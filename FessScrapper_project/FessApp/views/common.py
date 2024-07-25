from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .copy_docker_file import copy_file_from_container
from .move_docker_file import move_file_from_container
from .guardian import Fess_Gardian_Post
from .Deloitte import Fess_Deloitte_Post
from .sodalitas import fess_sodalitas_post
from .hbr import Fess_hbr_Post
from .economist import Fess_economist_Post
from .sharedvalue import Fess_Sharedvalue_Post
from .direct_insert import Fess_direct_insertView
from django.views.decorators.csrf import csrf_exempt
import logging
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logger = logging.getLogger(__name__)

# Create a ThreadPoolExecutor instance
executor = ThreadPoolExecutor(max_workers=10)  # Adjust max_workers as needed

@api_view(['POST'])
@csrf_exempt  # Be cautious using csrf_exempt in production
def Fess_split_Post(request):
    """
    Handle POST requests to save data and return the file path.
    """
    if request.method == 'POST':
        logger.info('Received POST request with data: %s', request.data)

        collection_name = request.data.get("collectionName", "").lower()
        body = request.data.get("article_content", "").lower()
        link = request.data.get("link")

        def handle_request():
            if not body:
                if 'guardian' in collection_name:
                    return Fess_Gardian_Post(request)
                elif 'deloitte' in collection_name:
                    return Fess_Deloitte_Post(request)
                elif 'sodalitas' in collection_name:
                    return fess_sodalitas_post(request)
                elif 'hbr' in collection_name:
                    return Fess_hbr_Post(request)
                elif 'economist' in collection_name:
                    return Fess_economist_Post(request)
                elif 'sharedvalue' in collection_name:
                    return Fess_Sharedvalue_Post(request)
                else:
                    logger.error('Invalid collection name: %s', collection_name)
                    raise ValueError("Invalid collection name")
            else:
                return Fess_direct_insertView(request)
                
        try:
            future = executor.submit(handle_request)
            full_path = future.result()  # Wait for the thread to complete and get the result

            logger.info('Data successfully saved to %s', full_path)
            return Response({"message": "Data successfully saved", "file_path": full_path}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error('Error processing request: %s', str(e), exc_info=True)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
