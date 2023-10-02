from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.status import HTTP_201_CREATED
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserRegisterSerializer
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Artist,Work
from .serializers import ArtistSerializer,WorkSerializer,UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated users to get tokens
def obtain_auth_token(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)

@permission_classes([AllowAny])
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email']
        )
        user.save()
        # Add any additional logic like sending a confirmation email here
        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def filter_works_by_artist(request):
    artist_name = request.GET.get('artist')
    if artist_name:
        filtered_works = Work.objects.filter(artist__name=artist_name)
        # You can serialize the filtered_works if needed
        data = {
            'results': [work.serialize() for work in filtered_works],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Missing artist parameter'}, status=400)
    

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def filter_works_by_work_type(request):
    work_type = request.GET.get('work_type')
    if work_type:
        filtered_works = Work.objects.filter(work_type=work_type)
        # You can serialize the filtered_works if needed
        data = {
            'results': [work.serialize() for work in filtered_works],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Missing work_type parameter'}, status=400)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ArtistDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class WorkListCreateView(generics.ListCreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class WorkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer