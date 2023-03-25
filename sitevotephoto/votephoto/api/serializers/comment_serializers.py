from rest_framework import serializers

from votephoto.mymodels.model_comment import Comment


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "pk",
            "content",
            "dateCreate",
            "dateUpdate",
            "Parent_id",
            "photo",
            "user",
        ]
