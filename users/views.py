from django.shortcuts import render
from .serializers import SignUpSerializer,ProfileSerializer, ProfileUpdateSerializer, PasswordChangeSerializer, LoginSerializer
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(SignUpSerializer(user).data)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response({'msg': 'me', 'data': serializer.data}, status=status.HTTP_200_OK)

    

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        serializer = ProfileUpdateSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'msg': 'Profile updated',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)



class PassChangeView(APIView):
    permission_classes = [IsAuthenticated, ]
    def put(self, request):
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data, context = {'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': 'Parol muvaffaqiyatli o\'zgartirildi'}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        Token.objects.filter(user=request.user).delete()

        return Response({
            'msg': 'Tizimdan chiqdingiz'
        }, status=status.HTTP_200_OK)
