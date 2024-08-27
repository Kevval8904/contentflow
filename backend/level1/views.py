from django.shortcuts import render

# Create your views here.


# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import requests
# from cloudinary import uploader
# import cloudinary
# from rest_framework.response import Response
# from rest_framework import status

# # Configure Cloudinary
# cloudinary.config(
#     cloud_name="dmbx6xwhq",
#     api_key="168946697938814",
#     api_secret="35E3DkoGHHz-qPaXFGVzwkWMVU0"
# )

# access_token = 'EAAHkyOTzrjcBOZB9lp84NtyK40UX1utVjJyDYKc5h3mDjkGskXUhAS0OZCwhAdD1NgflA35LdLhSULQzipkKBvplJHjS5ZBvvvVZBIsC1SZBBbnkqihhg5zHecEQ4Mhp6HgHADER8u9k5YqcsqbfHs1ngaaDqHEZCwojB7s8Fo5WqqmcsqZC41UP55WRhETSrSC'

# def fetch_facebook_page_id(request):
#     url = f'https://graph.facebook.com/v16.0/me/accounts?access_token={access_token}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if 'data' in data and len(data['data']) > 0:
#             page_id = data['data'][0]['id']
#             return JsonResponse({'page_id': page_id})
#     return JsonResponse({'error': 'Failed to fetch Facebook Page ID'}, status=400)

# def fetch_instagram_business_account_id(request, page_id):
#     url = f'https://graph.facebook.com/v16.0/{page_id}?fields=instagram_business_account&access_token={access_token}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         instagram_business_account = data.get('instagram_business_account')
#         if instagram_business_account:
#             instagram_business_id = instagram_business_account.get('id')
#             return JsonResponse({'instagram_business_id': instagram_business_id})
#     return JsonResponse({'error': 'Failed to fetch Instagram Business Account ID'}, status=400)

# @csrf_exempt
# def create_instagram_media(request):
#     if request.method == 'POST':
#         image_path = request.POST.get('image_path')
#         caption = request.POST.get('caption')
#         business_id = request.POST.get('business_id')

#         # Upload the image to Cloudinary
#         response = uploader.upload(image_path)
#         image_url = response.get('secure_url')

#         # Create media object
#         url = f'https://graph.facebook.com/v16.0/{business_id}/media'
#         params = {
#             'image_url': image_url,
#             'caption': caption,
#             'access_token': access_token
#         }
#         response = requests.post(url, params=params)
#         if response.status_code == 200:
#             data = response.json()
#             return JsonResponse({'creation_id': data.get('id')})
#     return JsonResponse({'error': 'Failed to create media object'}, status=400)

# @csrf_exempt
# def publish_instagram_media(request):
#     if request.method == 'POST':
#         creation_id = request.POST.get('creation_id')
#         business_id = request.POST.get('business_id')

#         # Publish media object
#         url = f'https://graph.facebook.com/v16.0/{business_id}/media_publish'
#         params = {
#             'creation_id': creation_id,
#             'access_token': access_token
#         }
#         response = requests.post(url, params=params)
#         if response.status_code == 200:
#             return JsonResponse({'success': True})
#     return JsonResponse({'error': 'Failed to publish media object'}, status=400)








# @api_view(['POST'])
# def upload_image(request):
#     file = request.FILES.get('file')
#     if not file:
#         return requests.Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Save the file to the default storage
#         file_name = default_storage.save(file.name, file)
#         file_path = default_storage.url(file_name)
        
#         # Upload to Cloudinary
#         response = cloudinary.uploader.upload(file_path)
#         image_url = response.get('secure_url')

#         # Post to Instagram (replace with your implementation)
#         access_token = 'EAAHkyOTzrjcBOZB9lp84NtyK40UX1utVjJyDYKc5h3mDjkGskXUhAS0OZCwhAdD1NgflA35LdLhSULQzipkKBvplJHjS5ZBvvvVZBIsC1SZBBbnkqihhg5zHecEQ4Mhp6HgHADER8u9k5YqcsqbfHs1ngaaDqHEZCwojB7s8Fo5WqqmcsqZC41UP55WRhETSrSC'
#         page_id = fetch_facebook_page_id(access_token)
        
#         if page_id:
#             business_id = fetch_instagram_business_account_id(page_id, access_token)
            
#             if business_id:
#                 caption = request.data.get('caption', 'Default caption')
#                 creation_id = create_instagram_media(business_id, access_token, image_url, caption)
                
#                 if creation_id:
#                     publish_instagram_media(business_id, creation_id, access_token)
                    
#         return Response({"message": "Image uploaded and posted to Instagram."}, status=status.HTTP_200_OK)
    
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # Include the necessary functions from your existing code here



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

# Configure Cloudinary
# cloudinary.config(
#     cloud_name="your_cloud_name", 
#     api_key="your_api_key",
#     api_secret="your_api_secret"
# )

# access_token = 'your_facebook_access_token'


# cloudinary.config(
#     cloud_name="dmbx6xwhq",
#     api_key="168946697938814",
#     api_secret="35E3DkoGHHz-qPaXFGVzwkWMVU0"
# )

# access_token = 'EAAHkyOTzrjcBOZB9lp84NtyK40UX1utVjJyDYKc5h3mDjkGskXUhAS0OZCwhAdD1NgflA35LdLhSULQzipkKBvplJHjS5ZBvvvVZBIsC1SZBBbnkqihhg5zHecEQ4Mhp6HgHADER8u9k5YqcsqbfHs1ngaaDqHEZCwojB7s8Fo5WqqmcsqZC41UP55WRhETSrSC'


# views.py

# import cloudinary
# import cloudinary.uploader
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.files.storage import default_storage
# from django.conf import settings
# import cloudinary
# import cloudinary.uploader
# from django.core.files.storage import default_storage
# from django.http import JsonResponse
# from rest_framework.decorators import api_view
# # Make sure Cloudinary is configured
# cloudinary.config(
#     cloud_name="dmbx6xwhq",
#     api_key="168946697938814",
#     api_secret="35E3DkoGHHz-qPaXFGVzwkWMVU0"
# )

# @csrf_exempt
# def upload_view(request):
#     if request.method == 'POST':
#         file = request.FILES.get('file')
#         caption = request.POST.get('caption')
        
#         if file:
#             try:
#                 # Save the file to the default storage
#                 file_name = default_storage.save(file.name, file)
#                 # Construct the full path to the file
#                 file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                
#                 # Print the full file path for debugging
#                 print(f"Full file path: {file_path}")

#                 # Upload to Cloudinary
#                 response = cloudinary.uploader.upload(file_path)
#                 image_url = response.get('secure_url')
                
#                 # Log details to the console
#                 print(f"Image URL: {image_url}")
#                 print(f"Caption: {caption}")
                
#                 # Proceed with the Instagram posting logic here...
                
#                 return JsonResponse({'message': 'File uploaded successfully', 'file_url': image_url, 'caption': caption})
            
#             except Exception as e:
#                 print(f"An error occurred: {e}")
#                 return JsonResponse({'error': 'Internal server error'}, status=500)
        
#         return JsonResponse({'error': 'No file uploaded'}, status=400)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# access_token = "EAAHkyOTzrjcBOZB9lp84NtyK40UX1utVjJyDYKc5h3mDjkGskXUhAS0OZCwhAdD1NgflA35LdLhSULQzipkKBvplJHjS5ZBvvvVZBIsC1SZBBbnkqihhg5zHecEQ4Mhp6HgHADER8u9k5YqcsqbfHs1ngaaDqHEZCwojB7s8Fo5WqqmcsqZC41UP55WRhETSrSC"
# def fetch_facebook_page_id():
#     url = f'https://graph.facebook.com/v16.0/me/accounts?access_token={access_token}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         if 'data' in data and len(data['data']) > 0:
#             return data['data'][0]['id']
#     return None

# def fetch_instagram_business_account_id(page_id):
#     url = f'https://graph.facebook.com/v16.0/{page_id}?fields=instagram_business_account&access_token={access_token}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         instagram_business_account = data.get('instagram_business_account')
#         if instagram_business_account:
#             return instagram_business_account.get('id')
#     return None

# def create_instagram_media(business_id, image_url, caption):
#     url = f'https://graph.facebook.com/v16.0/{business_id}/media'
#     params = {
#         'image_url': image_url,
#         'caption': caption,
#         'access_token': access_token
#     }
#     response = requests.post(url, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         return data.get('id')
#     return None

# def publish_instagram_media(business_id, creation_id):
#     url = f'https://graph.facebook.com/v16.0/{business_id}/media_publish'
#     params = {
#         'creation_id': creation_id,
#         'access_token': access_token
#     }
#     response = requests.post(url, params=params)
#     return response.status_code == 200



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.conf import settings
import cloudinary
import cloudinary.uploader
import requests
import os

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
