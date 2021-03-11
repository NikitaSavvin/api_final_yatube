from rest_framework import generics, permissions, filters, viewsets
from .serializers import PostSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly 
from .models import Post, User, Group, Follow, Comment
from .permissions import IsAuthorOrReadOnly 
from .serializers import CommentSerializer, PostSerializer, GroupSerializer, FollowSerializer
from rest_framework.generics import get_object_or_404

class PostViewSet(viewsets.ModelViewSet): 
    queryset = Post.objects.all()
    serializer_class = PostSerializer 
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly] 
    filter_backends = [DjangoFilterBackend]
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
            'created': self.kwargs.get('created', '') 
        } 
        serializer.save(**data) 
 
    def get_queryset(self): 
        post_id = self.kwargs.get('post_id', '') 
        post = get_object_or_404(Post, pk=post_id) 
        all_comments_of_post = post.comments.all() 
        return all_comments_of_post


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer 
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly] 
    http_method_names = ('get', 'post')


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer 
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username']
    http_method_names = ('get', 'post')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) 
 
    def get_queryset(self):    
        user = get_object_or_404(User, username=self.request.user)
        return Follow.objects.filter(following=user)
