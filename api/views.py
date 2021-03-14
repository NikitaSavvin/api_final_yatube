from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_fields = ['group', ]

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        data = {
            'author': self.request.user,
            'post': get_object_or_404(Post, pk=self.kwargs.get('post_id')),
            'created': serializer.fields['created']
        }
        serializer.save(**data)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        all_comments_of_post = post.comments.all()
        return all_comments_of_post


class GroupViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']
    http_method_names = ('get', 'post')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = user.following.all()
        return queryset
