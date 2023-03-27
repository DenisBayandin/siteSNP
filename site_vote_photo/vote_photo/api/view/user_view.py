from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


from ..serializers.user_serializers import UserRegisterSerializers, UserSerializers
from vote_photo.mymodels.model_user import User


class UsersView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializers = UserSerializers(users, many=True)
        return Response(serializers.data)

    def post(self, request, *args, **kwargs):
        serializers = UserRegisterSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            breakpoint()
            Token.objects.create(
                user_id=User.objects.get(username=request.data["username"]).id
            )
            return Response(serializers.data)
        return Response(serializers.errors)


class DetailUser(APIView):
    def get_objects(self, user_id):
        return get_object_or_404(User, id=user_id)

    def get(self, request, user_id, format=None):
        user = self.get_objects(user_id)
        serializers = UserSerializers(user)
        return Response(serializers.data)

    def put(self, request, user_id, format=None):
        user = self.get_objects(user_id)
        serializers = UserSerializers(user, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors)

    def delete(self, request, user_id, format=None):
        user = self.get_objects(user_id)
        token = Token.objects.get(user_id=user_id)
        token.delete()
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)
