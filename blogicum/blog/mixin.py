from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Comment
from .forms import CommentForm


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
