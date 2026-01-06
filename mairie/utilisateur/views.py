from django.shortcuts import render
from .models import User
from .serializer import UserSerializer, LoginSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field='id'
    
    @action(detail=False, methods=['post'], url_path='login', permission_classes=[permissions.AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            
            user_data = UserSerializer(user, context={"request": request}).data
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data
            })
        return Response({'detail': 'Identifiants invalides.'}, status=status.HTTP_404_NOT_FOUND)
    