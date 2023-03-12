from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic.list import ListView
from django.utils import timezone
from django.db.models import Q

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


class FeaturedListView(ListView):
    model = Post
    template_name = 'blogs/results.html'

    def get_queryset(self):
        query = Post.objects.filter(featured=True).filter(
            pub_date__lte=timezone.now()
        )
        return query


class CategoryListView(ListView):
    model = Post
    template_name = 'blogs/results.html' 

    def get_queryset(self):
        query = self.request.path
        post_list = Post.objects.filter(categories__slug=query).filter(
            pub_date__lte=timezone.now()
        )
        return post_list


class SearchResultsView(ListView):
    model = Post
    template_name = 'blogs/results.html' 

    def get_queryset(self):
        query = self.request.GET.get('search')
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query)
        ).filter(
            pub_date__lte=timezone.now()
        ).distinct()
        return post_list