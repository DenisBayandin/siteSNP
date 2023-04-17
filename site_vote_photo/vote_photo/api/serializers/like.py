from rest_framework import serializers

from vote_photo.models import Like


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "user", "photo", "date_create", "date_update"]
