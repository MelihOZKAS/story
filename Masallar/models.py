from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from Tales.custom_storages import ImageSettingStorage
from django.utils import timezone

status_cho = (
    ("Taslak", "Taslak"),
    ("Hazir", "Hazir"),
    ("Yayinda", "Yayinda"),
    ("oto", "oto"),
    ("manuel", "manuel"),
)
HELP_TEXTS = {
    "title": "Masal Hiyenin başlığını girin.",
    "h1": "İçeriğin H1 Seo uyumlu girilmesi Lazım.",
    "Model": "Modele göre sılanma ve konumlandırılma olacaktır.",
    "yazar": "Şiiri yazan kullanıcıyı seçin.",
    "slug": "Şiirin URL'de görünecek kısmını girin.",
    "kategorisi": "Şiirin kategorisini seçin.",
    "resim": "858 x 400",
    "icerik": "Şiirin içeriğini girin.",
    "kapak_resmi": "Anasayfa Resim",
    "status": "Şiirin durumunu seçin.",
    "aktif": "Şiirin aktif olup olmadığını belirtin.",
    "meta_title": "Sayfanın meta başlığını girin.",
    "meta_description": "Sayfanın meta açıklamasını girin.",
    "keywords": "Sayfanın anahtar kelimelerini \" Virgül '  ' \" ile ayrınız. ",
    "banner": "Ana Sayfadaki büyük resim alanında ögrünür",
    "small_banner": "Ana sayfada küçük resimlerde görünür.",
    "hakkinda": "Şiir hakkında anlatılmak istenen.",
    "Acikalama": "Kullanıcının işlem durumunu gösterir.",
    "Story Catagory": "Hikayenin kategorisi",
}
def kapak_resmi_upload_to(instance, filename):
    # Dosya adını değiştir
    yeni_ad = f"{instance.slug}"
    # Dosya uzantısını koru
    uzanti = filename.split('.')[-1]
    # Yeni dosya adını döndür
    return f"kapak_resimleri/{yeni_ad}.{uzanti}"


class StoryCategory(models.Model):
    Title = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, blank=True)
    H1 = models.CharField(max_length=255,blank=True, null=True)
    Hikaye_meta_description = models.TextField( blank=True, null=True, help_text=HELP_TEXTS["meta_description"])
    Hikaye_keywords = models.CharField(max_length=255,blank=True,null=True,help_text=HELP_TEXTS["keywords"])
    short_title = models.CharField(max_length=255, blank=True)
    ozet_kisa = models.CharField(max_length=255, blank=True)
    sirasi = models.IntegerField(default=100)
    Aktif = models.BooleanField(default=False)
    Banner = models.BooleanField(default=False)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Story Category"
    def __str__(self):
        return self.Title


# Create your models here.
class Story(models.Model):
    title = models.CharField(max_length=255, help_text=HELP_TEXTS["title"])
    slug = models.SlugField(max_length=255, unique=True, blank=True,help_text=HELP_TEXTS["slug"])
    h1 = models.CharField(max_length=255,blank=True, help_text=HELP_TEXTS["h1"])
    Hikaye_Turu = models.ForeignKey(StoryCategory, null=True, on_delete=models.SET_NULL)
    icerik = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    resim = models.ImageField(upload_to=kapak_resmi_upload_to,
                                    storage=ImageSettingStorage(),
                                    help_text=HELP_TEXTS["resim"], null=True, blank=True)
    youtube = models.URLField(blank=True)
    meta_description = models.TextField(blank=True,verbose_name="Meta Açıklama",help_text=HELP_TEXTS["meta_description"])
    keywords = models.CharField(max_length=255,blank=True,verbose_name="Anahtar Kelimeler",help_text=HELP_TEXTS["keywords"])
    yayin_tarihi = models.DateTimeField(null=True, blank=True, help_text="Postanın yayınlanacağı tarih ve saat")
    status = models.CharField(max_length=10, choices=status_cho, default="Taslak", help_text=HELP_TEXTS["status"])
    aktif = models.BooleanField(default=False, help_text=HELP_TEXTS["aktif"])
    banner = models.BooleanField(default=False, help_text=HELP_TEXTS["banner"])
    small_banner = models.BooleanField(default=False,help_text=HELP_TEXTS["small_banner"])
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    #olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    olusturma_tarihi = models.DateTimeField(default=timezone.now, editable=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Post"
    def __str__(self):
        return self.title



class Blog(models.Model):
    title = models.CharField(max_length=255, help_text=HELP_TEXTS["title"])
    slug = models.SlugField(max_length=255, unique=True, blank=True,help_text=HELP_TEXTS["slug"])
    h1 = models.CharField(max_length=255,blank=True, help_text=HELP_TEXTS["h1"])
    icerik = RichTextField(null=True, blank=True, help_text=HELP_TEXTS["icerik"])
    resim_name = models.CharField(max_length=255,null=True, help_text=HELP_TEXTS["title"])
    resim = models.ImageField(upload_to=kapak_resmi_upload_to,
                              storage=ImageSettingStorage(),
                              help_text=HELP_TEXTS["kapak_resmi"], null=True, blank=True)
    youtube = models.URLField(blank=True)
    meta_description = models.TextField(blank=True,verbose_name="Meta Açıklama",help_text=HELP_TEXTS["meta_description"])
    keywords = models.CharField(max_length=255,blank=True,verbose_name="Anahtar Kelimeler",help_text=HELP_TEXTS["keywords"])
    yayin_tarihi = models.DateTimeField(null=True, blank=True, help_text="Postanın yayınlanacağı tarih ve saat")
    status = models.CharField(max_length=10, choices=status_cho, default="Taslak", help_text=HELP_TEXTS["status"])
    aktif = models.BooleanField(default=False, help_text=HELP_TEXTS["aktif"])
    banner = models.BooleanField(default=False, help_text=HELP_TEXTS["banner"])
    small_banner = models.BooleanField(default=False,help_text=HELP_TEXTS["small_banner"])
    okunma_sayisi = models.PositiveBigIntegerField(default=0)
    #olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    olusturma_tarihi = models.DateTimeField(default=timezone.now, editable=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "BlogPost"
    def __str__(self):
        return self.title




class iletisimmodel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255,blank=True,null=True,help_text=HELP_TEXTS["keywords"])
    title = models.TextField( blank=True, null=True)
    icerik = models.TextField( blank=True, null=True, help_text=HELP_TEXTS["meta_description"])
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "iletişim Formu"
    def __str__(self):
        return self.title