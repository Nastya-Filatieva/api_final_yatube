from django.urls import path, include
from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("v1/posts", PostViewSet)
router.register(r"v1/posts/(?P<post_id>\d+)/comments", CommentViewSet)
router.register("v1/follow", FollowViewSet)
router.register("v1/groups", GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
