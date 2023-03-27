from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from vote_photo.mymodels.model_photo import Photo
from ..serializers.photo_serializers import AllPhotoSerializers, LoadPhotoSerializers


# from site_vote_photo.vote_photo.mymodels.model_photo import Photo


class AllPhotoView(APIView):
    def get(self, request, format=None):
        photo = Photo.objects.all()
        serializers = AllPhotoSerializers(photo, many=True)
        return Response(serializers.data)


class AllPhotoWithStateVerifiedView(APIView):
    def get(self, request, format=None):
        photo = Photo.objects.filter(state="Verified")
        serializers = AllPhotoSerializers(photo, many=True)
        return Response(serializers.data)


class OnePhotoView(APIView):
    def get_objects(self, id):
        return get_object_or_404(Photo, id=id)

    def get(self, request, id, format=None):
        photo = Photo.objects.get(id=id)
        serializers = AllPhotoSerializers(photo)
        return Response(serializers.data)


class LoadPhotoView(ListAPIView):
    def post(self, request, *args, **kwargs):
        image = request.data["old_photo"]
        serializer = LoadPhotoSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
