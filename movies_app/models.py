from django.db import models
from datetime import date
from django.urls import reverse
from PIL import Image


class Category(models.Model):
    name = models.CharField('Category_name', max_length=150)
    description = models.TextField('Category_Description', blank=True)
    url_film = models.SlugField(max_length=170, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']


class Actor(models.Model):
    name = models.CharField('Actor_name', max_length=150)
    birth_year = models.PositiveIntegerField('Birth_year', default=0)
    description = models.TextField('Actor_description', blank=True)
    image = models.ImageField('Actor_picture', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'
        ordering = ['id']


class Genre(models.Model):
    name = models.CharField('Genre_name', max_length=150)
    description = models.TextField('Genre_description', blank=True)
    url = models.SlugField(max_length=170, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['id']


class Language(models.Model):
    name = models.CharField('Languages_name', max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering = ['id']


class Movie(models.Model):
    title = models.CharField('Title', max_length=150)
    tagline = models.CharField('Tag', max_length=150, default='')
    description = models.TextField('Description', blank=True)
    poster = models.ImageField('Poster', upload_to='movies/')
    year = models.PositiveIntegerField('Publishing year', default=2020)
    country = models.CharField('Country', max_length=30)
    actors = models.ManyToManyField(
        Actor, verbose_name='Actors', related_name='Movie_actors')
    genres = models.ManyToManyField(Genre, verbose_name='Genres')
    world_premiere = models.DateField('Premiere', default=date.today().year)
    budget = models.PositiveIntegerField(
        'Movie_budget', default=0, help_text='Please enter movie_budget')
    for_url = models.SlugField(max_length=170, unique=True)
    movie_ctg = models.ManyToManyField(
        Category, verbose_name='Movie_category', related_name='Into_category')
    draft = models.BooleanField('Draft', default='False')
    base_language = models.ForeignKey(
        Language, verbose_name='Movie_base_language', on_delete=models.CASCADE, null=True)
    dubbing_language = models.ManyToManyField(
        Language, verbose_name='Movie_dubbing_language', related_name='into_languages')
    transcription_language = models.ManyToManyField(
        Language, verbose_name='Movie_transcription_language', related_name='into_language')
    directed_by = models.CharField(
        'Directors', max_length=150, null=True, blank=True)
    produced_by = models.CharField(
        'Producers', max_length=200, null=True, blank=True)
    written_by = models.CharField(
        'Writers', max_length=200, null=True, blank=True)
    imdb_rtg = models.FloatField('IMDB_rating', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={'slug': self.for_url})

    def get_comment(self):
        return self.comment_set.filter(parent__isnull=True)

    # deyisen.baglioldugumodelinfieldi for deyisen in self.movcudmodeldekifieldinadi.all()
    def show_movie_ctg(self):
        return "\n".join([ctg.name for ctg in self.movie_ctg.all()])

    def show_genre(self):
        return "\n".join([gnr.name for gnr in self.genres.all()])

    def get_dub_lan(self):
        return "\n".join([dl.name for dl in self.dubbing_language.all()])

    def get_trans_lan(self):
        return "\n".join([tl.name for tl in self.transcription_language.all()])

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'


class MovieShots(models.Model):
    title = models.CharField('Title', max_length=150)
    description = models.TextField('Description', blank=True)
    image = models.ImageField('Picture', upload_to='movie_shots/')
    movie = models.ForeignKey(
        Movie, verbose_name='MovieShots', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Movieshot'
        verbose_name_plural = 'Movieshots'

#    def save(self, *args, **kwargs):
#        super().save(*args, **kwargs)
#
#        img = Image.open(self.image.path)
#
#        if img.height > 200 or img.width > 200:
#            output_size = (200, 200)
#            img.thumbnail(output_size)
#            img.save(self.image.path)


class RatingStar(models.Model):
    value = models.PositiveSmallIntegerField('Rating_value', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Rating star'
        verbose_name_plural = 'Rating stars'


class Rating(models.Model):
    ip = models.CharField('IP adress', max_length=15)
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name='Rating')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, verbose_name='rating_movie')

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Comment(models.Model):
    email = models.EmailField()
    name = models.CharField('Name', max_length=100)
    text = models.TextField('Review_text', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Parent',
                                on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(
        Movie, verbose_name='Movie', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
