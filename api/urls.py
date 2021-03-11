from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken import views 
from rest_framework.routers import DefaultRouter    
from django.urls import path, include
from .views import (
    PostViewSet,
    CommentViewSet,
    FollowViewSet,
    GroupViewSet,
)

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
]