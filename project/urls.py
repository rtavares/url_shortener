"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from main.views import UrlShortenerView, UrlExpanderView

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('url_shortener_view'))),
    path('shorten_url/', UrlShortenerView.as_view(), name='url_shortener_view'),
    path('shorten_url/<str:shortened>', UrlExpanderView.as_view(), name='url_expand_view'),
    path('shorten_url/<path:url>', RedirectView.as_view(url=reverse_lazy('url_shortener_view'))),
    path('shorten_url/<str:url>', RedirectView.as_view(url=reverse_lazy('url_shortener_view'))),
    path('admin/', admin.site.urls),
]

