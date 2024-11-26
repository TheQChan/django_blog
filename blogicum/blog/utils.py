from blog.models import Post
from django.db.models import Q
from django.core.paginator import Paginator

from datetime import datetime

from .constants import MAX_PUB


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


def get_paginator(posts, request):
    paginator = Paginator(posts, MAX_PUB)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
