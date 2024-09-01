import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import json,time

logger = logging.getLogger(__name__)

# Set the scope for YouTube API
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRET_FILE = 'C:/Users/aagam shah/Documents/College Stuff/SEM-4/Projects/ContentFlow comb/contentflow/backend/level2/client_secret.json'


def get_authenticated_service():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        youtube = build('youtube', 'v3', credentials=credentials)
        return youtube
    except Exception as e:
        logger.error(f"Error during authentication: {e}")
        raise

@csrf_exempt
def upload_view(request):
    if request.method == 'POST':
        if 'video' not in request.FILES:
            return JsonResponse({'error': 'No video file found in the request'}, status=400)

        file = request.FILES['video']
        media_dir = os.path.join('media')
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        file_path = os.path.join(media_dir, file.name)
        # file_path=str(file_path)
        print(type(file_path))
        try:
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return JsonResponse({'error': 'Error saving the file'}, status=500)

        try:
            youtube = get_authenticated_service()
            title = request.POST.get('title', 'Untitled Video')
            description = request.POST.get('description', '')
            category = request.POST.get('category', '22')
            privacy_status = request.POST.get('privacy_status', 'public')

            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'categoryId': category
                },
                'status': {
                    'privacyStatus': privacy_status
                }
            }
            media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
            request = youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Uploaded {int(status.progress() * 100)}%")
                    print("i am here")
            # time.sleep(20)  # Wait for 20 seconds
            # os.remove(file_path)

            return JsonResponse({'video_id': response['id']})
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return JsonResponse({'error': f'Error uploading video: {str(e)}'}, status=500)
