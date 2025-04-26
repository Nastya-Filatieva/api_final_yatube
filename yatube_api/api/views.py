from rest_framework import viewsets
from posts.models import Post, Comment, Group, Follow, User
from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer
)
from rest_framework.exceptions import (
    PermissionDenied,
    MethodNotAllowed,
    ValidationError
)
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied()
        return super().perform_destroy(instance)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied()
        return super().perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=Post.objects.get(pk=self.kwargs['post_id'])
        )

    def get_queryset(self):
        return Comment.objects.filter(
            post=Post.objects.get(pk=self.kwargs['post_id'])
        )

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied()
        return super().perform_destroy(instance)

    def perform_update(self, serializer):
        if serializer.instance.author == self.request.user:
            serializer.save(author=self.request.user)
            return
        return super().perform_update(serializer)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed(method="POST", code=405)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if not self.request.data.get('following'):
            raise ValidationError()
        if Follow.objects.filter(
            user=self.request.user,
            following=User.objects.get(
                username=self.request.data.get('following')
            )
        ):
            raise ValidationError()
        if self.request.user == User.objects.get(
            username=self.request.data.get('following')
        ):
            raise ValidationError()
        serializer.save(
            user=self.request.user,
            following=User.objects.get(
                username=self.request.data.get('following')
            )
        )
