from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('kids-story-categories/', views.kategori, name='tüm_kategoriler'),#Hikaye Kategorileri
    path('new-kids-stories-added/', views.enson_eklenen_blog_list, name='en-son-eklenen'),#En Son Eklenenler
    path('most-read-childrens-stories/', views.cokokunan, name='en-cok-okunan'),#En çok okunan
    path('kids-stories-youtube-videos/', views.video, name='video'),#Youtube Videoları
    path('blog/', views.blog, name='blog'),#Blog

    path('contact/', views.iletisim, name='iletisim'),#Blog
    path('cookie-policy/', views.cerez, name='cerez'),#Blog
    path('privacy-policy/', views.gizlilik, name='gizlilik'),#Blog
    path('about/', views.hakkinda, name='hakkinda'),#Blog

    path('oto-add-categories/', views.oto_hikayekategoriekle),#Kategorileri otomatik ekler

    path('kids-story-categories-detail/<str:kategori_slug>/', views.kategori_icerik_list, name='kategori_detay'),#Kategorideki Hikayeler
    path('kids-bedtime-story/<str:story_slug>/', views.post_getir, name='postagit'),#Hikayeye Git
    path('blog/<str:blog_slug>/', views.blog_getir, name='blogGit'),#Blog Git
]