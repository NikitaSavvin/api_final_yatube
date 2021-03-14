from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

v1_router = DefaultRouter()


v1_router.register('posts', PostViewSet, basename='post')
v1_router.register('group', GroupViewSet, basename='group')
v1_router.register('follow', FollowViewSet, basename='follow')
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet, basename='comment'
)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
