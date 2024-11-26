from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView

from blog.models import Comment, Post, Category
from .forms import PostForm, CommentForm, ProfileEditForm
from .utils import getting_posts, get_paginator


User = get_user_model()


def index(request):
    template = 'blog/index.html'
    draft_posts = getting_posts()
    posts = draft_posts.annotate(
        comment_count=Count('comment')
    ).order_by('-pub_date')
    page_obj = get_paginator(posts, request)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post_queryset = Post.objects.filter(is_published=True)

    if request.user.is_authenticated:
        post_queryset = post_queryset | Post.objects.filter(
            author=request.user
        )

    post = get_object_or_404(post_queryset, pk=pk)
    comments = post.comment.all()
    context = {'post': post, 'comments': comments, 'form': CommentForm()}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    posts = getting_posts(category_slug).order_by('-pub_date')
    page_obj = get_paginator(posts, request)
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True
    )
    context = {'category': category, 'page_obj': page_obj}
    return render(request, template, context)


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'blog/create.html'
    model = Post
    form_class = PostForm

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user

    def handle_no_permission(self):
        post = self.get_object()
        return redirect(
            reverse_lazy('blog:post_detail', kwargs={'pk': post.id})
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )


class PostDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'blog/create.html'
    model = Post
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = (
        Post.objects.annotate(comment_count=Count('comment'))
        .filter(author=user)
        .order_by('-pub_date')
    )
    page_obj = get_paginator(posts, request)
    context = {'page_obj': page_obj, 'profile': user}
    return render(request, 'blog/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=pk)


class CommentMixin(UserPassesTestMixin):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'

    def get_object(self):
        comment_id = self.kwargs['comment_id']
        comment = get_object_or_404(
            Comment, pk=comment_id, post__id=self.kwargs['pk']
        )
        return comment

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['pk']}
        )


class CommentUpdateView(CommentMixin, UpdateView):
    pass


class CommentDeleteView(CommentMixin, DeleteView):
    pass
