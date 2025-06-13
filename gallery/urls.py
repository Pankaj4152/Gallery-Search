from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.ImageUpload.as_view(), name='upload'),
    path('image-list/', views.ImageList.as_view(), name='image_list'),
    path('search/', views.ImageSearch.as_view(), name='search_images'),
    path('delete/<int:image_id>/', views.ImageDelete.as_view(), name='delete_image'),
    path('delete_all/', views.DeleteAllImages.as_view(), name='delete_all_images'),
]