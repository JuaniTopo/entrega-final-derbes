from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils import timezone

from blogs.models import Post, Category

# Create your views here.

def home_page(request):
    posts = Post.objects.filter(
        pub_date__lte=timezone.now()
    )
    categories = Category.objects.all()
    featured = Post.objects.filter(featured=True).filter(
        pub_date__lte=timezone.now()
    )[:3]

    context = {
        'posts': posts,
        'categories': categories,
        'featured': featured
    }

    return render(request, 'blogs/home_page.html', context=context)


class PostDetailView(generic.DetailView):
    model = Post
    queryset = Post.objects.filter(
        pub_date__lte=timezone.now()
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class FeaturedListView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html'

    def get_queryset(self):
        query = Post.objects.filter(featured=True).filter(
        pub_date__lte=timezone.now()
        )
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.get_queryset()
        context['categories'] = Category.objects.all()
        return context

class CategoryListView(generic.ListView):
    model = Post
    template_name = 'blogs/results.html' 

    