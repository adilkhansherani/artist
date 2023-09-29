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
def get_artist_by_id(request, artist_id):
    try:
        artist_object = get_object_or_404(Artist, id=artist_id)
        # Now, work_object contains the object with the specified ID
        data = {
            'id': artist_object.id,  
            'name': artist_object.name,
            'user_id': artist_object.user_id,
            # Add other fields as needed
        }
        return JsonResponse(data)
    except Exception as e:
        # Handle exceptions, such as Work.DoesNotExist
        return JsonResponse({'error': str(e)}, status=404)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_work_by_id(request, work_id):
    try:
        work_object = get_object_or_404(Work, id=work_id)
        # Now, work_object contains the object with the specified ID
        data = {
            'id': work_object.id,  
            'link': work_object.link,
            'type': work_object.work_type,
            'artist_id': list(work_object.artist.values_list('id', flat=True)),
            # Add other fields as needed
        }
        return JsonResponse(data)
    except Exception as e:
        # Handle exceptions, such as Work.DoesNotExist
        return JsonResponse({'error': str(e)}, status=404)

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
