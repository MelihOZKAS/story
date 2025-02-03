from django.urls import path
from . import views
from django.views.generic.base import RedirectView
from django.urls import re_path


app_name = 'stories'  # Bu satırı ekleyin

urlpatterns = [
    path("", views.NewHome, name="home"),
    path('kids-story-categories/', views.kategori, name='tüm_kategoriler'),  # Hikaye Kategorileri
    path('new-kids-stories-added/', views.enson_eklenen_blog_list, name='en-son-eklenen'),  # En Son Eklenenler
    path('most-read-childrens-stories/', views.cokokunan, name='en-cok-okunan'),  # En çok okunan
    path('kids-stories-youtube-videos/', views.video, name='video'),  # Youtube Videoları
    path('mobill-app/', views.app, name='app'),
    path('testnewhome/', views.NewTestHome, name='yenihome'),
    path('ekle/', views.ekle, name='ekle'),
    path('blog/', views.blog, name='blog'),
    path("oto-shared/", views.Oto_Paylas),
    path("index-ver/", views.indexing_var_mi, name="indexver"),
    path("facebook-cek/", views.facebook_var_mi, name="facebookver"),
    path("linkedin-cek/", views.linkedin_var_mi, name="linkedincek"),
    path("twitter-cek/", views.twitter_var_mi, name="twitterver"),
    path("pint-cek/", views.pinterest_var_mi, name="pintver"),
    path("add-story/", views.apiyle_ekle),

    path('contact/', views.iletisim, name='iletisim'),
    path('cookie-policy/', views.cerez, name='cerez'),
    path('privacy-policy/', views.gizlilik, name='gizlilik'),
    path('about/', views.hakkinda, name='hakkinda'),
    path('story-preview/<slug:slug>/', views.StoryPreviewView.as_view(), name='story_preview'),

    path('oto-add-categories/', views.oto_hikayekategoriekle),
    path('kids-story-categories-detail/<str:kategori_slug>/', views.kategori_icerik_list, name='kategori_detay'),
    # Kategorideki Hikayeler
    # Eski URL'i yeni URL'e yönlendir
    path('blog/<str:blog_slug>/', views.blog_getir, name='blogGit'),
    # Eski URL'leri yeni URL'lere kalıcı yönlendir
    re_path(r'^kids-bedtime-story/(?P<story_slug>[\w-]+)/$',
            RedirectView.as_view(url='/%(story_slug)s/', permanent=True)),

    # Yeni URL
    path('<str:story_slug>/', views.post_getir, name='postagit'),
]
