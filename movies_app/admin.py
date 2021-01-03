
from django.contrib import admin
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Comment, Language
from django.utils.safestring import mark_safe
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url_film")
    list_display_links = ("name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("name", "birth_year", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Image"


class ReviewInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Image"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "show_movie_ctg", "for_url", "draft",)
    list_filter = ("year", "movie_ctg")
    search_fields = ("title", "movie_ctg")
    inlines = [MovieShotsInline, ReviewInline]
    actions = ["publish", "unpublish"]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    readonly_fields = ("get_image",)
    form = MovieAdminForm
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster", "get_image")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country", "produced_by", "written_by"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directed_by", "genres", "movie_ctg", "imdb_rtg"),)
        }),
        (None, {
            "fields": (("budget", "base_language", "dubbing_language", "transcription_language"),)
        }),
        ("Options", {
            "fields": (("for_url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, queryset):
        if row_update == 1:
            message_bit = '1 record uptated'
        else:
            message_bit = f"{row_update} records uptated"
        self.message_user(request, f"{message_bit}")

    def publish(self, queryset):
        if row_update == 1:
            message_bit = '1 record uptated'
        else:
            message_bit = f"{row_update} records uptated"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Publish"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Unpublish"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Poster"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("title", "movie", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Image"


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
