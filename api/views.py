from django.shortcuts import get_object_or_404

from api.models import Follow, Group, Post
from api.permission import OwnPermission
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from django_filters import rest_framework
from rest_framework import filters, generics, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnPermission)
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_fields = ('group',)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, OwnPermission)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        comments = post.comments.all()
        return comments

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class FollowViewSet(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnPermission)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class GroupViewSet(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnPermission)
