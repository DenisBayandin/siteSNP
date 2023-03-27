from rest_framework import serializers

from vote_photo.mymodels.model_comment import Comment


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
