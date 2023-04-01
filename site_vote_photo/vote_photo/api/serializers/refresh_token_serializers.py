from rest_framework import serializers


class RefreshTokenSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
