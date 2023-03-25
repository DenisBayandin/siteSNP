from rest_framework import serializers

from votephoto.mymodels.model_photo import Photo


class AllPhotoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = [
            "pk",
            "name",
            "content",
            "date_create",
            "count_like",
            "count_comment",
            "user",
            "state",
        ]


class LoadPhotoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["pk", "name", "content", "old_photo", "user"]
