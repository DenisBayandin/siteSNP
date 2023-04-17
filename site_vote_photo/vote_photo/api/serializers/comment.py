from rest_framework import serializers

from vote_photo.models import Comment


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "date_create",
            "date_update",
            "parent",
            "photo",
            "user",
        ]


class AutoSwaggerShcemeCommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "content",
            "parent",
        ]
