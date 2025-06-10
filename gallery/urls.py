from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'gallery', views.GalleryView, 'gallery')

urlpatterns = [
    path('upload/', views.ImageUpload, name='upload'),
    path('image_list/', views.ImageList, name='image_list'),
    path('search/', views.ImageSearch, name='search_images'),
    path('delete/<int:image_id>/', views.ImageDelete, name='delete_image'),
    path('delete_all/', views.DeleteAllImages, name='delete_all_images'),
]