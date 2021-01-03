from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from .forms import CommentForm

from .models import Movie,Category
# Create your views here.


class MovieView(ListView):

    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies_app/movies.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['categories'] = Category.objects.all()
        return context

class MovieDetailView(DetailView):

    model = Movie
    slug_field = 'for_url'
    #template_name = 'movies_app/movie_detail.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AddCommentView(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent",None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
