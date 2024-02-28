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

class StoryAnimals(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True,Hikaye_Turu__short_title="Animals", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])

class StoryResponsibility(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Responsibility", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])

class StoryFamily(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Family", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])

class StoryBravery(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Bravery & Courage", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])
class StorySisters(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Sisters", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])

class StoryFairyTales(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Fairy Tales", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])

class StoryMagic(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Magic", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])

class StoryFathers(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Fathers", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])


class StoryProblem(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Problem Solving", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])

class StoryMothers(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Mothers", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])



class StoryFriendship(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Story.objects.filter(aktif=True, Hikaye_Turu__short_title="Friendship", status="Yayinda")

    def lastmod(self, obj):
        return obj.guncelleme_tarihi

    def location(self, obj):
        return reverse('postagit', args=[obj.slug])