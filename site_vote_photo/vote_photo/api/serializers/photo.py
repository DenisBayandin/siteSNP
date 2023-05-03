from rest_framework import serializers

from vote_photo.models import Photo


class AllPhotoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [
            "id",
            "name",
            "content",
            "date_create",
            "count_like",
            "count_comment",
            "user",
            "state",
        ]


class LoadPhotoSerializers(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Photo
        fields = ["id", "name", "content", "old_photo", "user"]


class UpdatePhotoYesPhotoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["name", "content", "new_photo"]


class UpdatePhotoNoPhotoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["name", "content", "old_photo"]


class UpdatePhotoSerializers(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = Photo
        fields = ["name", "content", "new_photo"]
