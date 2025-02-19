"""
URL configuration for Tales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.sitemaps.views import index, sitemap
from Masallar.views import *
from .sitemaps import *

sitemaps = {
    'Story-Categories': StoryCategorySitemap,
    'Story': StorySitemap,
    'Blog-Post': BlogSitemap,
    'Kids-Bedtime-Story': StoryBedtime,
    'Kids-Animals-Story': StoryAnimals,
    'Kids-Responsibility-Story': StoryResponsibility,
    'Kids-Family-Story': StoryFamily,
    'Kids-Bravery-Courage-Story': StoryBravery,
    'Kids-Sisters-Story': StorySisters,
    'Kids-Fairy-Tales-Story': StoryFairyTales,
    'Kids-Magic-Story': StoryMagic,
    'Kids-Fathers-Story': StoryFathers,
    'Kids-Problem-Solving-Story': StoryProblem,
    'Kids-Mothers-Story': StoryMothers,
    'Kids-Friendship-Story': StoryFriendship,
}


def handler404(request, *args, **argv):
    response = render(request, '404.html')
    response.status_code = 404
    return response


urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('sitemap.xml/', index, {'sitemaps': sitemaps}),
                  path('sitemap-<section>.xml/', sitemap, {'sitemaps': sitemaps},
                       name='django.contrib.sitemaps.views.sitemap'),
                  path("robots.txt/", robots_txt, name="robots"),
                  path("Ads.txt/", ads, name="ads"),
                  path("ads.txt/", ads, name="ads"),
                  path("", include("Masallar.urls")),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
