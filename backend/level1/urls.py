# from django.urls import path
# from . import views

# urlpatterns = [
#     path('fetch_facebook_page_id/', views.fetch_facebook_page_id, name='fetch_facebook_page_id'),
#     path('fetch_instagram_business_account_id/<str:page_id>/', views.fetch_instagram_business_account_id, name='fetch_instagram_business_account_id'),
#     path('create_instagram_media/', views.create_instagram_media, name='create_instagram_media'),
#     path('publish_instagram_media/', views.publish_instagram_media, name='publish_instagram_media'),
# ]

from django.urls import path
from .views import upload_view

urlpatterns = [
    path('upload/', upload_view, name='upload'),
]