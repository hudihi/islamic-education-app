from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'videos', views.VideoViewSet)
router.register(r'books', views.BookViewSet)
router.register(r'posters', views.PosterViewSet)

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    
    # API URLs
    path('api/', include(router.urls)),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Video Management
    path('videos/', views.video_list, name='video_list'),
    path('videos/upload/', views.upload_video, name='upload_video'),
    path('videos/<int:pk>/edit/', views.edit_video, name='edit_video'),
    path('videos/<int:pk>/delete/', views.delete_video, name='delete_video'),
    
    # Book Management
    path('books/', views.book_list, name='book_list'),
    path('books/upload/', views.upload_book, name='upload_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    
    # Poster Management
    path('posters/', views.poster_list, name='poster_list'),
    path('posters/upload/', views.upload_poster, name='upload_poster'),
    path('posters/<int:pk>/edit/', views.edit_poster, name='edit_poster'),
    path('posters/<int:pk>/delete/', views.delete_poster, name='delete_poster'),
]
