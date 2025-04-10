from django.contrib import admin

from .models import Video, Book, Poster

# Register your models here.
admin.site.register(Video)
admin.site.register(Book)
admin.site.register(Poster)
