from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Video, Book, Poster


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'category', 'image', 'file']


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'image', 'file']


class PosterForm(ModelForm):
    class Meta:
        model = Poster
        fields = ['title', 'description', 'image']

# class MultiUploadForm(forms.Form):
#     video_files = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
#     book_files = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
#     poster_files = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}), required=False)
