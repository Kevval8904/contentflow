import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import cloudinary
import cloudinary.uploader
import requests

logger = logging.getLogger(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name="dmbx6xwhq",
    api_key="168946697938814",
    api_secret="35E3DkoGHHz-qPaXFGVzwkWMVU0"
)

# Your access token for Facebook/Instagram API
access_token = "EAAHkyOTzrjcBOZB9lp84NtyK40UX1utVjJyDYKc5h3mDjkGskXUhAS0OZCwhAdD1NgflA35LdLhSULQzipkKBvplJHjS5ZBvvvVZBIsC1SZBBbnkqihhg5zHecEQ4Mhp6HgHADER8u9k5YqcsqbfHs1ngaaDqHEZCwojB7s8Fo5WqqmcsqZC41UP55WRhETSrSC"

@csrf_exempt
def upload_view(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        caption = request.POST.get('caption', '')

        if not file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        try:
            # Save the file to default storage
            file_name = default_storage.save(file.name, file)
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            # Upload to Cloudinary
            response = cloudinary.uploader.upload(file_path)
            image_url = response.get('secure_url')

            # Fetch Facebook Page ID
            page_id = fetch_facebook_page_id()
            if not page_id:
                return JsonResponse({'error': 'Failed to fetch Facebook Page ID'}, status=400)

            # Fetch Instagram Business Account ID
            business_id = fetch_instagram_business_account_id(page_id)
            if not business_id:
                return JsonResponse({'error': 'Failed to fetch Instagram Business Account ID'}, status=400)

            # Create Instagram media object
            creation_id = create_instagram_media(business_id, image_url, caption)
            if not creation_id:
                return JsonResponse({'error': 'Failed to create Instagram media object'}, status=400)

            # Publish Instagram media
            success = publish_instagram_media(business_id, creation_id)
            if not success:
                return JsonResponse({'error': 'Failed to publish Instagram media'}, status=400)

            return JsonResponse({'message': 'Image uploaded and posted to Instagram.', 'file_url': image_url, 'caption': caption})

        except Exception as e:
            logger.error(f"An error occurred during Instagram upload: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)

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
