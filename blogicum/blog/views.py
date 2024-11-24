from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from datetime import datetime
from blog.models import Post, Category
from blog.constants import POST_LIMIT


def getting_posts(category_slug=None):
    time_now = datetime.now()
    posts = Post.objects.filter(
        pub_date__date__lt=time_now,
        is_published=True,
    ).filter(
        Q(category__slug=category_slug)
        if category_slug
        else Q(category__is_published=True)
    )
    return posts


def index(request):
    template = "blog/index.html"
    draft_posts = getting_posts()
    posts = (draft_posts.order_by("-pub_date"))[:POST_LIMIT]
    context = {"post_list": posts}
    return render(request, template, context)


def post_detail(request, id):
    template = "blog/detail.html"
    draf_posts = getting_posts()
    posts = get_object_or_404(
        draf_posts,
        pk=id,
    )
    context = {"post": posts}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    posts = getting_posts(category_slug)
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    context = {"category": category, "post_list": posts}
    return render(request, template, context)
