from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics, viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import PosterForm, VideoForm, BookForm, UserRegistrationForm
from .models import Video, Book, Poster
from .serializers import VideoSerializer, BookSerializer, PosterSerializer


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


# Create your views here.
def upload_poster(request):
    if request.method == 'POST':
        form = PosterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_poster')
    else:
        form = PosterForm()
    return render(request, 'app/upload_poster.html', {'form': form})


def upload_video(request):
    # if request.method == 'POST':
    form = VideoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('upload_video')
    else:
        form = VideoForm()
    return render(request, 'app/upload_video.html', {'form': form})


def upload_book(request):
    form = BookForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return redirect('upload_book')
    else:
        form = BookForm()
    return render(request, 'app/upload_book.html', {'form': form})


# views to handle API requests
class VideoList(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class PosterList(generics.ListAPIView):
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']  # Default ordering

    def get_queryset(self):
        queryset = Video.objects.all()
        category = self.request.query_params.get('category', None)
        featured = self.request.query_params.get('featured', None)

        if category:
            queryset = queryset.filter(category=category)
        if featured == 'true':
            queryset = queryset.filter(category=Video.FEATURED)

        return queryset


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PosterViewSet(viewsets.ModelViewSet):
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@login_required
def dashboard(request):
    recent_videos = Video.objects.all().order_by('-created_at')[:5]
    recent_books = Book.objects.all().order_by('-created_at')[:5]
    recent_posters = Poster.objects.all().order_by('-created_at')[:5]
    
    context = {
        'recent_videos': recent_videos,
        'recent_books': recent_books,
        'recent_posters': recent_posters,
        'video_count': Video.objects.count(),
        'book_count': Book.objects.count(),
        'poster_count': Poster.objects.count(),
        'featured_count': Video.objects.filter(category=Video.FEATURED).count(),
    }
    return render(request, 'dashboard.html', context)


@login_required
def video_list(request):
    videos = Video.objects.all().order_by('-created_at')
    return render(request, 'video_list.html', {'videos': videos})


@login_required
def upload_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        video_file = request.FILES.get('file')
        
        if title and category and image and video_file:
            video = Video.objects.create(
                title=title,
                category=category,
                image=image,
                file=video_file
            )
            messages.success(request, 'Video uploaded successfully!')
            return redirect('video_list')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    categories = Video.CATEGORY_CHOICES
    return render(request, 'upload_video.html', {'categories': categories})


@login_required
def edit_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            messages.success(request, 'Video updated successfully!')
            return redirect('video_list')
    else:
        form = VideoForm(instance=video)
    
    context = {
        'form': form,
        'video': video,
        'categories': Video.VIDEO_CHOICES,
    }
    return render(request, 'edit_video.html', context)


@login_required
def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.method == 'POST':
        video.delete()
        messages.success(request, 'Video deleted successfully.')
        return redirect('video_list')
    return redirect('video_list')


@login_required
def book_list(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'book_list.html', {'books': books})


@login_required
def upload_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        book_file = request.FILES.get('file')
        
        if title and description and image and book_file:
            book = Book.objects.create(
                title=title,
                description=description,
                image=image,
                file=book_file
            )
            messages.success(request, 'Book uploaded successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    return render(request, 'upload_book.html')


@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'edit_book.html', {'form': form, 'book': book})


@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully.')
        return redirect('book_list')
    return redirect('book_list')


@login_required
def poster_list(request):
    posters = Poster.objects.all().order_by('-created_at')
    return render(request, 'poster_list.html', {'posters': posters})


@login_required
def upload_poster(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        if title and description and image:
            poster = Poster.objects.create(
                title=title,
                description=description,
                image=image
            )
            messages.success(request, 'Poster uploaded successfully!')
            return redirect('poster_list')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    return render(request, 'upload_poster.html')


@login_required
def edit_poster(request, pk):
    poster = get_object_or_404(Poster, pk=pk)
    
    if request.method == 'POST':
        form = PosterForm(request.POST, request.FILES, instance=poster)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poster updated successfully!')
            return redirect('poster_list')
    else:
        form = PosterForm(instance=poster)
    
    return render(request, 'edit_poster.html', {'form': form, 'poster': poster})


@login_required
def delete_poster(request, pk):
    poster = get_object_or_404(Poster, pk=pk)
    if request.method == 'POST':
        poster.delete()
        messages.success(request, 'Poster deleted successfully.')
        return redirect('poster_list')
    return redirect('poster_list')
