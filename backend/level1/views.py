from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import cloudinary
import cloudinary.uploader
import requests
import os
from django.http import JsonResponse
from django.conf import settings


# Configure Cloudinary
cloudinary.config(
    cloud_name="dmbx6xwhq",
    api_key="168946697938814",
    api_secret="35E3DkoGHHz-qPaXFGVzwkWMVU0"
)

# Your access token
access_token = "EAAHkyOTzrjcBOZB9lp84NtyK40UX1utVjJyDYKc5h3mDjkGskXUhAS0OZCwhAdD1NgflA35LdLhSULQzipkKBvplJHjS5ZBvvvVZBIsC1SZBBbnkqihhg5zHecEQ4Mhp6HgHADER8u9k5YqcsqbfHs1ngaaDqHEZCwojB7s8Fo5WqqmcsqZC41UP55WRhETSrSC"

@csrf_exempt
def upload_view(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        caption = request.POST.get('caption')
        
        if file:
            try:
                # Save the file to the default storage
                file_name = default_storage.save(file.name, file)
                # Construct the full path to the file
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                
                # Print the full file path for debugging
                print(f"Full file path: {file_path}")

                # Upload to Cloudinary
                response = cloudinary.uploader.upload(file_path)
                image_url = response.get('secure_url')
                
                # Log details to the console
                print(f"Image URL: {image_url}")
                print(f"Caption: {caption}")
                
                # Fetch Facebook Page ID
                page_id = fetch_facebook_page_id()
                if not page_id:
                    return JsonResponse({'error': 'Failed to fetch Facebook Page ID'}, status=400)

                print(f"Facebook Page ID: {page_id}")

                # Fetch Instagram Business Account ID
                business_id = fetch_instagram_business_account_id(page_id)
                if not business_id:
                    return JsonResponse({'error': 'Failed to fetch Instagram Business Account ID'}, status=400)

                print(f"Instagram Business Account ID: {business_id}")

                # Create Instagram media object
                creation_id = create_instagram_media(business_id, image_url, caption)
                if not creation_id:
                    return JsonResponse({'error': 'Failed to create Instagram media object'}, status=400)

                print(f"Media Creation ID: {creation_id}")

                # Publish Instagram media
                success = publish_instagram_media(business_id, creation_id)
                if not success:
                    return JsonResponse({'error': 'Failed to publish Instagram media'}, status=400)

                return JsonResponse({'message': 'Image uploaded and posted to Instagram.', 'file_url': image_url, 'caption': caption})

            except Exception as e:
                print(f"An error occurred: {e}")
                return JsonResponse({'error': 'Internal server error'}, status=500)
        
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def fetch_facebook_page_id():
    url = f'https://graph.facebook.com/v16.0/me/accounts?access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            return data['data'][0]['id']
    return None

def fetch_instagram_business_account_id(page_id):
    url = f'https://graph.facebook.com/v16.0/{page_id}?fields=instagram_business_account&access_token={access_token}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        instagram_business_account = data.get('instagram_business_account')
        if instagram_business_account:
            return instagram_business_account.get('id')
    return None

def create_instagram_media(business_id, image_url, caption):
    url = f'https://graph.facebook.com/v16.0/{business_id}/media'
    params = {
        'image_url': image_url,
        'caption': caption,
        'access_token': access_token
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('id')
    return None

def publish_instagram_media(business_id, creation_id):
    url = f'https://graph.facebook.com/v16.0/{business_id}/media_publish'
    params = {
        'creation_id': creation_id,
        'access_token': access_token
    }
    response = requests.post(url, params=params)
    return response.status_code == 200












import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

logger = logging.getLogger(__name__)

# Set the scope for YouTube API
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRET_FILE = 'client_secret.json'

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
            os.remove(file_path)
            return JsonResponse({'video_id': response['id']})
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return JsonResponse({'error': f'Error uploading video: {str(e)}'}, status=500)
