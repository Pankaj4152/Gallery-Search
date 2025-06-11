from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegisterUser.as_view(), name='signup'),
]