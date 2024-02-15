from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from Masallar.models import *

class StoryCategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.3
    protocol = 'https'

    def items(self):
        return StoryCategory.objects.all()

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('kategori_detay', args=[obj.slug])


class StorySitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True,status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])







class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Blog.objects.filter(aktif=True,status="Yayinda")
    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('blogGit', args=[obj.slug])




class StoryBedtime(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True,Hikaye_Turu__short_title="Bedtime Stories", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])