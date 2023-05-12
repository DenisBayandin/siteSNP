from rest_framework import serializers


class AutoSwaggerShcemeFilterPhotoSerializers(serializers.Serializer):
    filter_photo = serializers.CharField()


class AutoSwaggerShcemeGetPhotoIdFromCommentSerializers(serializers.Serializer):
    photo_id = serializers.CharField()


class AutoSwaggerShcemeGetPhotoIdFromLikeSerializers(serializers.Serializer):
    photo_id = serializers.CharField()
