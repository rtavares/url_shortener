from django.contrib import admin

# Register your models here.

from .models import UrlShortened

admin.site.register(UrlShortened)
