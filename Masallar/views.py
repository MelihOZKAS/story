from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views import View
from django.db.models import Q
from django.db.models import F
import requests
import environ
import random
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseBadRequest, \
    HttpResponseServerError
import json
from django.db.utils import IntegrityError



from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.db.models import Prefetch, Count
from django.conf import settings

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()


def create_unique_title_slug(title):
    slug = slugify(title)
    unique_slug = slug
    unique_title = title
    num = 1
    while Story.objects.filter(slug=unique_slug).exists() or Story.objects.filter(title=unique_title).exists():
        unique_slug = '{}-{}'.format(slug, num)
        unique_title = '{} {}'.format(title, num)
        num += 1
    return unique_title, unique_slug


def get_youtube_id(url):
    # YouTube video URL'sinden video ID'sini çıkaran bir regex deseni
    link = url.replace("https://www.youtube.com/embed/", "")
    youtube_id = link.split("?")
    return youtube_id[0] if youtube_id else None


# Create your views here.
def home(request):
    title = "Bedtime Stories for Kids of All Ages - KidsStoriesHub"
    description = "Explore KidsStoriesHub.com for captivating bedtime stories. Dive into a world of imagination and learning with our vast collection of stories for children."
    keywords = "bedtime story, story, bedtime stories for kids, short bedtime stories, bedtime stories to read online, bedtime stories to read online free, free bedtime stories, story for kids, story books, short story bedtime stories to read, bedtime story books, kids books online"

    endStory = Story.objects.filter(aktif=True, status="Yayinda").order_by('-olusturma_tarihi')[:8]
    story_categories = StoryCategory.objects.filter(Aktif=True, Banner=True)[
                       :6]  # Banner=True olan StoryCategory nesnelerini alır
    colors = ['primary', 'secondary', 'tertiary', 'quaternary', 'senary']
    categories_with_colors = []
    for index, category in enumerate(story_categories):
        color = colors[index % len(colors)]
        categories_with_colors.append((category, color))

    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'endStory': endStory,
        'categories_with_colors': categories_with_colors,
    }
    return render(request, 'Hepsi/home.html', context)


def NewHome(request):
    Categories_ALL = StoryCategory.objects.filter(story__aktif=True, story__status="Yayinda").annotate(
        story_count=Count('story'))

    title = "Bedtime Stories for Kids of All Ages - KidsStoriesHub"
    description = "Explore KidsStoriesHub.com for captivating bedtime stories. Dive into a world of imagination and learning with our vast collection of stories for children."
    keywords = "bedtime story, story, bedtime stories for kids, short bedtime stories, bedtime stories to read online, bedtime stories to read online free, free bedtime stories, story for kids, story books, short story bedtime stories to read, bedtime story books, kids books online"
    Random_Story = Story.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    endStory = Story.objects.filter(aktif=True, status="Yayinda").order_by('-olusturma_tarihi')[:8]
    story_categories = StoryCategory.objects.filter(Aktif=True, Banner=True)[
                       :6]  # Banner=True olan StoryCategory nesnelerini alır
    colors = ['primary', 'secondary', 'tertiary', 'quaternary', 'senary']
    categories_with_colors = []
    for index, category in enumerate(story_categories):
        color = colors[index % len(colors)]
        categories_with_colors.append((category, color))

    context = {
        'Categories_ALL': Categories_ALL,
        'Random_Story': Random_Story,
        'title': title,
        'description': description,
        'keywords': keywords,
        'endStory': endStory,
        'categories_with_colors': categories_with_colors,
    }
    return render(request, 'Hepsi/NewHome.html', context)

@cache_page(60 * 15)  # 15 dakika cache
def NewTestHome(request):
    cache_key = 'home_page_data_optimized'
    context = cache.get(cache_key)

    if not context:
        # Son 8 Hikaye (Sadece Gerekli Alanlar)
        latest_stories = (
            Story.objects
            .filter(aktif=True, status="Yayinda")
            .select_related('Hikaye_Turu')  # ForeignKey için optimize
            .only(
                'h1',
                'slug',
                'olusturma_tarihi',
                'Hikaye_Turu__short_title',  # İlişkili modelden alan
                'Hikaye_Turu__slug'
            )
            .order_by('-olusturma_tarihi')[:8]
        )

        # Tüm Kategoriler (Sıralı ve Sadeleştirilmiş)
        categories = (
            StoryCategory.objects
            .order_by(F('sirasi').asc(nulls_last=True))  # NULL'ları sona at
            .only('short_title', 'slug')
        )

        # SEO Meta
        meta = {
            'title': "Bedtime Stories for Kids - KidsStoriesHub",
            'description': "Discover magical bedtime stories for children...",
            'keywords': "bedtime stories, kids stories, short stories"
        }

        context = {
            'latest_stories': latest_stories,
            'categories': categories,
            **meta
        }

        cache.set(cache_key, context, 60 * 15)



    return render(request, 'newbase.html', context)

def kategori(request):
    Categories_ALL = StoryCategory.objects.filter(story__aktif=True, story__status="Yayinda").annotate(
        story_count=Count('story'))
    Random_Story = Story.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    title = "Explore Various Categories of Bedtime Stories | Read & Listen Free"
    H1 = "Discover a World of Bedtime Stories"
    description = "Dive into our diverse collection of bedtime stories. Explore tales of friendship, motherhood, problem-solving, and exciting animal adventures."
    keywords = "Bedtime Stories, Children's Literature, Educational Stories, Friendship Tales, Animal Adventures, Motherhood Stories, Problem-Solving Narratives, Inspirational Stories, Moral Stories, Fantasy Tales"

    context = {
        'title': title,
        'H1': H1,
        'description': description,
        'keywords': keywords,
        'Categories_ALL': Categories_ALL,
        'Random_Story': Random_Story,
    }
    return render(request, 'Hepsi/categories-all.html', context)


def blog(request):
    Story_ALL = Blog.objects.filter(aktif=True, status="Yayinda").order_by('-olusturma_tarihi')
    Categories_ALL = StoryCategory.objects.filter(story__aktif=True, story__status="Yayinda").annotate(
        story_count=Count('story'))
    Random_Story = Story.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    title = "Bedtime Stories Blog for Kids at KidsStoriesHub.com"
    H1 = "Bedtime Stories Blog for Children"
    description = "Explore our blog at KidsStoriesHub.com for engaging bedtime stories and tips. Dive into the world of imagination and learn the art of storytelling."
    keywords = "bedtime stories, kids blog, children’s blog, English stories, kids bedtime stories, storytelling tips, educational blog, bedtime tales, storytime blog, kids literature"

    paginator = Paginator(Story_ALL, 10)  # 10 içerik göstermek için
    page_number = request.GET.get('page')
    Story_ALL = paginator.get_page(page_number)

    if page_number is None:
        title = f"{title}"
        description = f"{description}"
    else:
        title = f"{title} - {page_number}"
        description = f"{description} - Page {page_number}"

    context = {
        'title': title,
        'H1': H1,
        'description': description,
        'sagUst': "Blog Post List",
        'keywords': keywords,
        'Story_ALL': Story_ALL,
        'Categories_ALL': Categories_ALL,
        'Random_Story': Random_Story,
    }
    return render(request, 'Hepsi/Blog-blog_list.html', context)


def kategori_icerik_list(request, kategori_slug):
    story_categori = get_object_or_404(StoryCategory, slug=kategori_slug)
    Story_ALL = Story.objects.filter(aktif=True, status="Yayinda", Hikaye_Turu=story_categori).order_by(
        '-guncelleme_tarihi')[:100]
    Categories_ALL = StoryCategory.objects.filter(story__aktif=True, story__status="Yayinda").annotate(
        story_count=Count('story'))
    Random_Story = Story.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    title = story_categori.Title
    H1 = story_categori.H1
    description = story_categori.Hikaye_meta_description
    keywords = story_categori.Hikaye_keywords

    paginator = Paginator(Story_ALL, 10)  # 10 içerik göstermek için
    page_number = request.GET.get('page')
    Story_ALL = paginator.get_page(page_number)

    if page_number is None:
        title = f"{title}"
        description = f"{description}"
    else:
        title = f"{title} - {page_number}"
        description = f"{description} - Page {page_number}"

    context = {
        'title': title,
        'H1': H1,
        'sagUst': story_categori.short_title,
        'description': description,
        'keywords': keywords,
        'Story_ALL': Story_ALL,
        'Categories_ALL': Categories_ALL,
        'Random_Story': Random_Story,
    }
    return render(request, 'Hepsi/blog_list.html', context)


def enson_eklenen_blog_list(request):  # Tamam...
    Story_ALL = Story.objects.filter(aktif=True, status="Yayinda").order_by('-guncelleme_tarihi')[:100]
    Categories_ALL = StoryCategory.objects.filter(story__aktif=True, story__status="Yayinda").annotate(
        story_count=Count('story'))
    Random_Story = Story.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]

    title = "Newly Added Children’s Stories | KidsStoriesHub.com"
    H1 = "Newly Added Magical Stories for Children"
    description = "Explore the newest collection of captivating stories for kids on KidsStoriesHub.com. Dive into a world of imagination and adventure with our latest tales."
    keywords = "kids stories, latest stories, children’s tales, kids literature, new stories, English stories, kids books, storytime, educational stories, bedtime stories”"

    paginator = Paginator(Story_ALL, 10)  # 10 içerik göstermek için
    page_number = request.GET.get('page')
    Story_ALL = paginator.get_page(page_number)

    if page_number is None:
        title = f"{title}"
        description = f"{description}"
    else:
        title = f"{title} - {page_number}"
        description = f"{description} - Page {page_number}"
        H1 = f"{H1} - Page {page_number}"

    context = {
        'title': title,
        'sagUst': "New Added",
        'H1': H1,
        'description': description,
        'keywords': keywords,
        'Story_ALL': Story_ALL,
        'Categories_ALL': Categories_ALL,
        'Random_Story': Random_Story,
    }
    return render(request, 'Hepsi/blog_list.html', context)


def cokokunan(request):  # Tamam
    Story_ALL = Story.objects.filter(aktif=True, status="Yayinda").order_by('-okunma_sayisi')[:100]
    Categories_ALL = StoryCategory.objects.filter(story__aktif=True, story__status="Yayinda").annotate(
        story_count=Count('story'))
    Random_Story = Story.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    title = "Top Children’s Stories: Most Read & Loved Tales for Kids"
    H1 = "Most Popular Children’s Stories"
    description = "Discover the top children’s stories that are loved and cherished by kids worldwide. These popular tales for children are a must-read!"
    keywords = "top children’s stories, popular children’s stories, loved tales, kids' favorites, must-read children’s stories"

    paginator = Paginator(Story_ALL, 10)  # 10 içerik göstermek için
    page_number = request.GET.get('page')
    Story_ALL = paginator.get_page(page_number)

    if page_number is None:
        title = f"{title}"
        description = f"{description}"
    else:
        title = f"{title} - {page_number}"
        description = f"{description} - Page {page_number}"
        H1 = f"{H1} - Page {page_number}"

    context = {
        'title': title,
        'H1': H1,
        'sagUst': "Most Read",
        'description': description,
        'keywords': keywords,
        'Story_ALL': Story_ALL,
        'Categories_ALL': Categories_ALL,
        'Random_Story': Random_Story,
    }
    return render(request, 'Hepsi/blog_list.html', context)


def video(request):  # Tamam
    Story_ALL = Story.objects.filter(aktif=True, status="Yayinda", youtube__isnull=False).exclude(
        youtube__exact='').order_by('-olusturma_tarihi')
    Categories_ALL = StoryCategory.objects.filter(story__aktif=True, story__status="Yayinda").annotate(
        story_count=Count('story'))
    Random_Story = Story.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    title = "Bedtime Stories with Videos for Kids on KidsStoriesHub.com"
    H1 = "Bedtime Video Stories for Children"
    description = "Immerse your child in the world of dreams with our bedtime video stories at KidsStoriesHub.com. Experience the magic of storytelling like never before."
    keywords = "bedtime stories, video stories, kids videos, children’s videos, English stories, kids bedtime stories, storytime videos, educational videos, bedtime tales, animated stories"

    paginator = Paginator(Story_ALL, 10)  # 10 içerik göstermek için
    page_number = request.GET.get('page')
    Story_ALL = paginator.get_page(page_number)

    if page_number is None:
        title = f"{title}"
        description = f"{description}"
    else:
        title = f"{title} - {page_number}"
        description = f"{description} - Page {page_number}"
        H1 = f"{H1} - Page {page_number}"

    context = {
        'title': title,
        'sagUst': "Youtube Story",
        'H1': H1,
        'description': description,
        'keywords': keywords,
        'Story_ALL': Story_ALL,
        'Categories_ALL': Categories_ALL,
        'Random_Story': Random_Story,
    }
    return render(request, 'Hepsi/blog_list.html', context)


def post_getir(request, story_slug):
    GelenPostStory = get_object_or_404(Story, slug=story_slug)
    thumbnail_url = None

    GelenPostStory.okunma_sayisi += 1
    GelenPostStory.save(update_fields=['okunma_sayisi'])

    Categories_ALL = StoryCategory.objects.filter(story__aktif=True, story__status="Yayinda").annotate(
        story_count=Count('story'))
    Random_Story = Story.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    title = GelenPostStory.title
    H1 = GelenPostStory.h1
    description = GelenPostStory.meta_description
    keywords = GelenPostStory.keywords
    Tur = "Story"

    category_names_str = GelenPostStory.Hikaye_Turu.short_title

    contents = [GelenPostStory.icerik, GelenPostStory.icerik2, GelenPostStory.icerik3]
    articleBody = ' '.join(filter(None, contents))

    resimler = []
    if GelenPostStory.resim:
        resimler.append(GelenPostStory.resim.url)
    if GelenPostStory.resim2:
        resimler.append(GelenPostStory.resim2.url)
    if GelenPostStory.resim3:
        resimler.append(GelenPostStory.resim3.url)
    if GelenPostStory.resim4:
        resimler.append(GelenPostStory.resim4.url)
    if GelenPostStory.resim5:
        resimler.append(GelenPostStory.resim5.url)
    if GelenPostStory.resim6:
        resimler.append(GelenPostStory.resim6.url)
    if GelenPostStory.resim7:
        resimler.append(GelenPostStory.resim7.url)
    if GelenPostStory.resim8:
        resimler.append(GelenPostStory.resim8.url)
    if GelenPostStory.resim9:
        resimler.append(GelenPostStory.resim9.url)
    if GelenPostStory.resim10:
        resimler.append(GelenPostStory.resim10.url)
    if not resimler:  # Eğer resimler listesi boşsa
        resimler.append("{% static 'images/bedtime-story.png' %}")

    if GelenPostStory.youtube:
        youtube_id = get_youtube_id(GelenPostStory.youtube)
        thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/0.jpg"

    if not GelenPostStory:
        category_names_str = "Bedtime Story"

    context = {
        'Tur': Tur,
        'title': title,
        'H1': H1,
        'description': description,
        'keywords': keywords,
        'Categories_ALL': Categories_ALL,
        'Random_Story': Random_Story,
        'GelenPostStory': GelenPostStory,
        'TumKategori': category_names_str,
        'thumbnail_url': thumbnail_url,
        'resimler': resimler,
        'articleBody': articleBody,
    }
    return render(request, 'Hepsi/enderun.html', context)


def blog_getir(request, blog_slug):
    GelenPostStory = get_object_or_404(Blog, slug=blog_slug)
    thumbnail_url = None

    # Increment the okunma_sayisi field by 1
    GelenPostStory.okunma_sayisi += 1
    GelenPostStory.save(update_fields=['okunma_sayisi'])

    Categories_ALL = StoryCategory.objects.filter(story__aktif=True, story__status="Yayinda").annotate(
        story_count=Count('story'))
    Random_Story = Story.objects.filter(aktif=True, status="Yayinda").order_by('?')[:8]
    title = GelenPostStory.title
    H1 = GelenPostStory.h1
    description = GelenPostStory.meta_description
    keywords = GelenPostStory.keywords
    Tur = "Blog"

    contents = [GelenPostStory.icerik, GelenPostStory.icerik2, GelenPostStory.icerik3]
    articleBody = ' '.join(filter(None, contents))

    resimler = []
    if GelenPostStory.resim:
        resimler.append(GelenPostStory.resim.url)
    if GelenPostStory.resim2:
        resimler.append(GelenPostStory.resim2.url)
    if GelenPostStory.resim3:
        resimler.append(GelenPostStory.resim3.url)
    if GelenPostStory.resim4:
        resimler.append(GelenPostStory.resim4.url)
    if GelenPostStory.resim5:
        resimler.append(GelenPostStory.resim5.url)
    if GelenPostStory.resim6:
        resimler.append(GelenPostStory.resim6.url)

    if not resimler:  # Eğer resimler listesi boşsa
        resimler.append("{% static 'images/bedtime-story.png' %}")

    if GelenPostStory.youtube:
        youtube_id = get_youtube_id(GelenPostStory.youtube)
        thumbnail_url = f"https://img.youtube.com/vi/{youtube_id}/0.jpg"

    context = {
        'Tur': Tur,
        'title': title,
        'H1': H1,
        'description': description,
        'keywords': keywords,
        'Categories_ALL': Categories_ALL,
        'Random_Story': Random_Story,
        'GelenPostStory': GelenPostStory,
        'TumKategori': Tur,
        'thumbnail_url': thumbnail_url,
        'resimler': resimler,
        'articleBody': articleBody,
    }
    return render(request, 'Hepsi/enderun.html', context)


@csrf_exempt
def oto_hikayekategoriekle(request):
    # Eklemek istediğiniz öğelerin listesi
    short_title = ["Friendship", "Mothers", "Problem Solving", "Fathers", "Magic", "Fairy Tales", "Sisters",
                   "Bravery & Courage", "Family", "Responsibility", "Bedtime Stories", "Animals"]
    short_H1 = ["Discover Heartwarming Kids' Bedtime Stories Filled with Themes of Friendship and Camaraderie",
                "Embrace Heartwarming Bedtime Moments with Kids' Stories Starring Loving Mothers",
                "Explore Bedtime Kids' Stories Focused on Creative Problem Solving",
                "Discover Heartwarming Bedtime Stories Featuring Beloved Father Figures for Kids",
                "Experience Enchanting Bedtime Stories Full of Magic for Kids",
                "Explore Magical Bedtime Fairy Tales for Kids A World of Imagination Awaits",
                "Enjoy Heartwarming Bedtime Stories with Sisterly Bonds A World of Adventures Awaits",
                "Dive into Inspiring Bedtime Stories of Bravery and Courage Where Bedtime Meets Heroic Tales",
                "Discover Bedtime Adventures with Family Uniting Loved Ones Through Heartwarming Stories",
                "Bedtime Stories on Responsibility Guiding Kids Towards a Sense of Duty and Care",
                "Bedtime Stories with a Touch of Magic Entertaining and Educational Stories for Kids",
                "Discover Enchanting Kids' Bedtime Stories Filled with Animal Characters"]
    Slug = ["kids-bedtime-friendship-stories", "mothers-kids-bedtime-stories",
            "problem-solving-bedtime-stories-for-kids", "fathers-bedtime-stories-for-kids",
            "magic-bedtime-stories-for-kids", "fairy-tales-bedtime-stories-for-kids", "sisters-kids-bedtime-stories",
            "bravery-courage-bedtime-stories-for-kids", "family-kids-bedtime-stories",
            "responsibility-bedtime-stories-for-kids", "kids-bedtime-stories", "kids-bedtime-stories-about-animals"]
    title = ["Kids Friendship Tales for Bedtime | Read & Listen Free",
             "Mother's Love Kids Bedtime Stories | Read & Listen Free",
             "Problem-Solving Kids Bedtime Tales | Read & Listen Free",
             "Father's Role: Kids Bedtime Stories | Read & Listen Free",
             "Magical Tales for Kids at Bedtime | Read & Listen Free",
             "Fairy Tales for Kids at Bedtime | Read & Listen Free",
             "Sisterhood in Kids Bedtime Stories | Read & Listen Free",
             "Bravery & Courage in Bedtime Tales | Read & Listen Free",
             "Family Love in Kids Bedtime Stories | Read & Listen Free",
             "Teaching Responsibility Bedtime Stories | Read & Listen Free",
             "Enchanting Bedtime Stories for Kids | Read & Listen Free",
             "Kids Bedtime Stories About Animals | Read & Listen Free"]
    desc = [
        "Discover the power of true friendship with heartwarming friendship stories. Explore the bonds of camaraderie and loyalty that warm your heart.",
        "Explore the love, sacrifices, and nurturing warmth of motherhood through heart-touching mothers' stories. Celebrate the essence of maternal bonds.",
        "Dive into captivating tales of ingenious solutions and life lessons in these problem-solving stories. Discover the art of overcoming challenges.",
        "Explore heartwarming tales that celebrate fathers' love, wisdom, and enduring bonds. Discover the beauty of fatherhood in these stories.",
        "Embark on enchanting adventures and discover the allure of magic in captivating stories. Let your imagination soar with these magical tales.",
        "Delve into a world of wonder with timeless fairy tales. Immerse yourself in enchanting stories filled with magic, heroes, and adventure.",
        "Discover enchanting stories celebrating the unbreakable bonds of sisterhood. Explore tales of love, loyalty, and shared adventures.",
        "Explore captivating Bravery & Courage stories showcasing remarkable feats, resilience, and heroic acts of valor. Find inspiration in tales of bravery.",
        "Discover Family Stories celebrating love, unity, and cherished moments. Delve into heartwarming tales of togetherness and adventures.",
        "Embrace Responsibility Stories, highlighting accountability, ethics, and valuable life lessons. Explore narratives of duty, morals, and personal growth.",
        "Immerse in enchanting Bedtime Stories, offering soothing tales and dreams that captivate young hearts. Discover a world of wonder and tranquility.",
        "Discover the enchanting world of animals through our bedtime stories. Dive into adventures and learn valuable lessons from the animal kingdom."]
    short_desc = ["Stories of friendship teach children valuable lessons about camaraderie.",
                  "Stories about mothers highlight the love and sacrifice of a mother.",
                  "Problem-solving stories teach children how to tackle challenges.",
                  "Stories about fathers showcase what fathers can do for their children.",
                  "Magic stories expand children’s imagination and transport them to a magical world.",
                  "Fairy tales take children to a fantastical and magical world.",
                  "Stories about sisters emphasize the bond and love between siblings.",
                  "Stories of bravery and courage teach children how to face their fears.",
                  "Family stories emphasize the importance of familial bonds and love.",
                  "Stories about responsibility teach children how to fulfill their duties.",
                  "Bedtime stories soothe children and prepare them for sleep.",
                  "Explore captivating animal tales and learn about nature."]

    # Listelerin aynı uzunlukta olduğunu kontrol et
    assert len(short_title) == len(short_H1) == len(Slug) == len(title) == len(desc)

    for i in range(len(short_title)):
        # Eğer bu masal zaten varsa, geç
        if StoryCategory.objects.filter(short_title=short_title[i]).exists():
            continue

        # Yeni bir MasalKategorileri örneği oluştur
        yeni_hikaye = StoryCategory(
            Title=title[i],
            slug=Slug[i],
            H1=short_H1[i],
            Hikaye_meta_description=desc[i],
            ozet_kisa=short_desc[i],
            sirasi=i,
            short_title=short_title[i],
            Aktif=True
        )

        # Yeni masalı veritabanına kaydet
        yeni_hikaye.save()

    return HttpResponse('Hikayeler başarıyla eklendi.')


def iletisim(request):
    context = {
        'title': "Enchanting Kids Bedtime Stories - Contact Us",
        'description': "Explore the enchanting world of kids’ bedtime stories with us. Your unforgettable bedtime experience starts here. Kids Fairy Tales Story",
        'keywords': "Kids Bedtime Stories,Children’s Literature,Magical Tales,Bedtime Reading,Story Time,Kids Books,Fairy Tales,Adventure Stories,Educational Stories,Fantasy Stories",

    }

    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': f"{env('RECAPTCHA_PRIVATE_KEY')}",
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            name = request.POST.get('InputName')
            email = request.POST.get('InputEmail')
            title = request.POST.get('InputSubject')
            icerik = request.POST.get('InputMessage')

            iletisim_obj = iletisimmodel(name=name, email=email, title=title, icerik=icerik)
            iletisim_obj.save()

            return HttpResponse(
                'We have recorded your contact request.<a href="{}" class="btn btn-primary">Click here to return to the homepage</a>'.format(
                    reverse('home')))
        else:
            return HttpResponse(
                'Human Control Error! <a href="{}" class="btn btn-primary">Click here to return to the Content</a>'.format(
                    reverse('iletisim')))

    return render(request, 'Hepsi/iletisim.html', context)


def cerez(request):
    title = "Kids’ Bedtime Stories - Cookie Policy"
    description = "Our cookie policy ensures a sweet experience while you journey through the world of kids’ bedtime stories. Learn more about our use of cookies."
    keywords = "bedtime stories for kids,short bedtime stories,bedtime stories to read online,bedtime stories to read online free,free bedtime stories,story for kids,story books,short story bedtime stories to read,bedtime story books,kids books online,short bedtime stories free,bedtime stories to read free,online stories,bedtime stories to read,bed story"

    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
    }
    return render(request, 'Hepsi/cerez.html', context)


def gizlilik(request):
    title = "Kids’ Bedtime Stories - Privacy Policy"
    description = "Navigate through our kids’ bedtime stories with peace of mind. Our privacy policy ensures your adventures are safe and secure. Magic story"
    keywords = "bedtime stories to read online,bedtime stories to read online free,free bedtime stories,story for kids,story books,short story bedtime stories to read,bedtime story books,kids books online"

    context = {
        'title': title,
        'description': description,
        'keywords': keywords,

    }
    return render(request, 'Hepsi/gizlilik.html', context)


def hakkinda(request):
    title = "About Us - Kids’ Bedtime Stories"
    description = "Learn more about our mission to bring enchanting kids’ bedtime stories to life. We’re dedicated to sparking imagination and dreams."
    keywords = "kids books online,short bedtime stories free,bedtime stories to read free,online stories,bedtime stories to read,bed story"

    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
    }
    return render(request, 'Hepsi/hakkinda.html', context)


@require_GET
def robots_txt(request):
    return HttpResponse(robots_txt_content, content_type="text/plain")

def app(request):
    title = "Mobil App- Kids Stories Hub - Free Kids Story Read"
    description = "Kids Stories Hub Free fairy tales and new edu games, %100 free mobil app - Kids Story Tales And Free Games"
    keywords = "mobil app, Kids Stort, Free Story, kids story"
    h1 = "Mobile App Free Downloand"
    context = {
        'title': title,
        'description': description,
        'keywords': keywords,
        'h1': h1,
    }
    return render(request, 'Hepsi/app.html', context)

robots_txt_content = """
User-agent: *
Allow: /
Sitemap: https://www.kidsstorieshub.com/sitemap.xml
"""


def Oto_Paylas(request):
    post = Story.objects.filter(Q(status="oto") & (Q(yayin_tarihi__lte=timezone.now()) | Q(yayin_tarihi=None))).first()

    if post is not None:
        post.status = "Yayinda"
        post.resimText = ""
        post.aktif = True
        post.indexing = True  # indekslendi olarak işaretle
        post.olusturma_tarihi = timezone.now()  # eklenme tarihini güncelle
        post.save()
        return HttpResponse(f'Şükürler Olsun "{post.title}" Paylaşıldı.')
    else:
        return HttpResponse('Paylaşılacak Post Bulunamadı.')


@csrf_exempt
def indexing_var_mi(request):
    post = Story.objects.filter(indexing=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un indexing durumunu False yapayı unutmamak lazımmm dimi.
        post.indexing = False
        post.save()
        return HttpResponse(f"https://www.kidsstorieshub.com/kids-bedtime-story/{post.slug}/")
    else:
        return HttpResponse("post bulunamadı.")


def ads(request):
    return HttpResponse(ads_content, content_type="text/plain")


ads_content = """google.com, pub-7065951693101615, DIRECT, f08c47fec0942fa0"""


@csrf_exempt
def apiyle_ekle(request):
    if request.method == 'POST':
        # Gelen POST isteğindeki değerleri alın
        title = request.POST.get('title')
        icerik = request.POST.get('icerik')
        kategorisi = request.POST.get('kategorisi')
        key = request.POST.get('kew')
        uzunluk = request.POST.get('uzunluk')

        hikaye_turu = StoryCategory.objects.get(short_title=kategorisi)

        title, slug = create_unique_title_slug(title)
        siir_masal = Story(title=title, Hikaye_Turu=hikaye_turu, icerik=icerik, slug=slug, keywords=key,
                           status="Taslak", uzunluk=uzunluk)
        siir_masal.save()
        if siir_masal.id is None:
            return HttpResponse("Model kaydedilemedi.")
        else:
            return HttpResponse("Model başarıyla kaydedildi. ID: " + str(siir_masal.id))


class StoryPreviewView(View):
    def get(self, request, *args, **kwargs):
        story = Story.objects.get(slug=kwargs['slug'])
        return HttpResponse(story.icerik)


@csrf_exempt
def facebook_var_mi(request):
    post = Story.objects.filter(facebook=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un facebook durumunu False yapayı unutmamak lazımmm dimi.
        post.facebook = False
        icerik = post.h1
        if not icerik:
            icerik = "%100 Free kids stories"
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinte'])
        return HttpResponse(
            f"https://www.kidsstorieshub.com/kids-bedtime-story/{post.slug}/!={icerik} You can visit our website for more children's fairy tales and stories!")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def linkedin_var_mi(request):
    post = Story.objects.filter(linkedin=True, aktif=True, status="Yayinda").order_by('-guncelleme_tarihi').first()
    if post is not None:
        # post'un facebook durumunu False yapayı unutmamak lazımmm dimi.
        post.linkedin = False
        icerik = post.h1
        if not icerik:
            icerik = "Haberin devamı için tıklayın!"
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'linkedin', 'pinte'])
        return HttpResponse(
            f"https://www.kidsstorieshub.com/kids-bedtime-story/{post.slug}/!={icerik} You can visit our website for more children's fairy tales and stories!")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def pinterest_var_mi(request):
    post = Story.objects.filter(pinte=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un facebook durumunu False yapayı unutmamak lazımmm dimi.
        post.pinte = False
        icerik = post.h1
        if not icerik:
            icerik = "%100 Free kids stories"
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinte'])
        return HttpResponse(
            f"https://www.kidsstorieshub.com/kids-bedtime-story/{post.slug}/!={icerik} You can visit our website for more children's fairy tales and stories!!={post.title}!={post.Hikaye_Turu.short_title}!={post.resim.url}")
    else:
        return HttpResponse("post bulunamadı.")


@csrf_exempt
def twitter_var_mi(request):
    post = Story.objects.filter(twitter=True, aktif=True, status="Yayinda").first()
    if post is not None:
        # post'un indexing durumunu False yapayı unutmamak lazımmm dimi.
        post.twitter = False
        icerik = post.h1
        kategorisi = post.Hikaye_Turu
        hashtag = "#" + kategorisi.short_title if kategorisi.short_title else ""
        if not icerik:
            icerik = "Free Kids Stories"
        post.save(update_fields=['okunma_sayisi', 'indexing', 'facebook', 'twitter', 'pinte'])
        return HttpResponse(
            f"https://www.kidsstorieshub.com/kids-bedtime-story/{post.slug}/!={icerik} {hashtag.replace(' ', '')} Click here to read this children's story for free!")
    else:
        return HttpResponse("Paylaşılacak Twitter içerik bulunamadı")




@csrf_exempt
def ekle(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method")

    # Gelen verileri al
    title = request.POST.get('title')
    h1 = request.POST.get('h1')
    slug = request.POST.get('slug')
    description = request.POST.get('description')
    keywords = request.POST.get('keywords')
    ozet = request.POST.get('ozet')
    sss = request.POST.get('sss')
    resim = request.POST.get('resim')
    content1 = request.POST.get('content1')
    content2 = request.POST.get('content2')
    content3 = request.POST.get('content3')
    content4 = request.POST.get('content4')
    content5 = request.POST.get('content5')
    content6 = request.POST.get('content6')
    content7 = request.POST.get('content7')
    content8 = request.POST.get('content8')
    content9 = request.POST.get('content9')
    content10 = request.POST.get('content10')

    # short_title al ve kategori belirle
    short_title = request.POST.get('short_title')
    kategori = None
    if short_title == "bedtime":
        kategori = StoryCategory.objects.filter(short_title="Bedtime Stories").first()
    elif short_title == "peri":
        kategori = StoryCategory.objects.filter(short_title="Fairy Tales").first()
    elif short_title == "macera":
        kategori = StoryCategory.objects.filter(short_title="macera-masallari").first()
    elif short_title == "hayvan":
        kategori = StoryCategory.objects.filter(short_title="Animals").first()
    elif short_title == "magic":
        kategori = StoryCategory.objects.filter(short_title="Magic").first()

    if resim:
        resim = f"3D cinematic film (caricature:0 2) [[{resim}]]"

    # Gerekli alanların doğrulanması
    if not title or not slug:
        return HttpResponseBadRequest("Title and slug are required")

    try:
        # Yeni bir Post oluştur
        post = Story.objects.create(
            title=title,
            h1=h1,
            slug=slugify(title),
            meta_description=description,
            keywords=keywords,
            resimText=resim,
            icerik=content1,
            icerik2=content2,
            icerik3=content3,
            icerik4=content4,
            icerik5=content5,
            icerik6=content6,
            icerik7=content7,
            icerik8=content8,
            icerik9=content9,
            icerik10=content10,
            Hikaye_Turu=kategori,
        )

        # Slug çakışmalarını engelle
        for _ in range(5):  # 5 deneme hakkı
            try:
                post.save()
                break
            except IntegrityError:
                random_number = random.randint(3, 100)
                post.slug = f"{slugify(slug)}-{random_number}" if slug else f"{slugify(title)}-{random_number}"


        # Başarı yanıtı
        return JsonResponse({
            "status": "success",
            "message": "Post created successfully",
            "post_id": post.id,
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)