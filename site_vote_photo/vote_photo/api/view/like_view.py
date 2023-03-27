from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.like_serializers import LikeSerializers
from vote_photo.mymodels.model_like import Like


class LikesView(APIView):

    # def get_objects(self, like_id):
    #     return get_object_or_404(Like, photo=photo_id, user=user_id)

    def get(self, request, photo_id, format=None):
        likes = Like.objects.filter(photo=photo_id)
        serializers = LikeSerializers(likes, many=True)
        return Response(serializers.data)

    def post(self, request, photo_id, *args, **kwargs):
        try:
            like = Like.objects.get(photo=photo_id, user=int(request.data["user"]))
        except ObjectDoesNotExist:
            serializers = LikeSerializers(
                data=(request.data.dict() | {"photo": photo_id})
            )
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data)
            return Response(serializers.errors)
        like.delete()
        return Response(
            "Удалили лайк,"
            " так как вы пытаетесь создать лайк к фотографии,"
            " который уже существует у данного юзера."
        )


class OneLikeView(APIView):
    def get_objects(self, like_id):
        return get_object_or_404(Like, id=like_id)

    def get(self, request, like_id, format=None):
        like = self.get_objects(like_id)
        serializers = LikeSerializers(like)
        return Response(serializers.data)

    def delete(self, request, like_id, format=None):
        like = self.get_objects(like_id)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
