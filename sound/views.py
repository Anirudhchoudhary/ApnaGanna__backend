from django.shortcuts import render 
from .serializers import SoundSerializer , AlbumSerializer , SoundDetailSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, CreateAPIView
from .models import Sound , Album
from rest_framework import status 
from rest_framework.authentication import SessionAuthentication , BasicAuthentication
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes , authentication_classes , throttle_classes
from rest_framework.views import APIView
from accounts.models import UserProfile
from .pagination import StandardResultsSetPagination
from rest_framework.permissions import IsAuthenticated , IsAdminUser
# Caching the data
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
# THROTTLING
from rest_framework.throttling import AnonRateThrottle , UserRateThrottle
# Create your views here.


class Hello(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        context = {
            "hello":"Anirudh",
        }
        return Response(data = context , status = status.HTTP_200_OK)


class SoundList(ListAPIView):
    throttle_classes = [AnonRateThrottle , UserRateThrottle]
    model = Sound
    allowed_methods = ["GET"]
    serializer_class = SoundSerializer
    queryset = Sound.objects.all()
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination



    @method_decorator(cache_page(60*60*12))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class SoundDetails(RetrieveAPIView):
    model = Sound
    serializer_class = SoundDetailSerializer
    slug_field = 'pk'
    queryset = Sound.objects.all()
    permission_classes = [AllowAny]



class SoundUpdate(RetrieveUpdateAPIView):
    model = Sound
    serializer_class = SoundSerializer
    queryset = Sound.objects.all()
    slug_field = 'pk'
    permission_classes = [IsAdminUser,IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            sound = get_object_or_404(Sound, pk=kwargs['pk'])
        except Sound.DoesNotExists:
            pass
        serializer = SoundSerializer(instance=sound)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        sound = get_object_or_404(Sound, pk=kwargs['pk'])
        serializer = SoundSerializer(sound, data=request.data, partial=True)
        if(serializer.is_valid()):
            sound = serializer.save()
            return Response(SoundSerializer(sound).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SoundDelete(RetrieveDestroyAPIView):
    model = Sound
    serializer_class = SoundSerializer
    slug_field = 'pk'
    queryset = Sound.objects.all()
    permission_classes = [IsAdminUser,IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.clean_fields())
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SoundCreate(CreateAPIView):
    model = Sound
    serializer_class = SoundSerializer
    slug_field = 'pk'
    permission_classes = []
    queryset = Sound.objects.all()
    permission_classes = []



@api_view(["POST"])
@permission_classes([])
@throttle_classes([AnonRateThrottle])
def updateplay(request , pk):
    if(request.method == "POST"):
        try:
            song = get_object_or_404(Sound , pk=pk)
        except Sound.DoesNotExist:
            data = {
                "message":"Obejct Does not exist with this pk",
                "status":status.HTTP_400_BAD_REQUEST,

            }
            return Response(data = data)
        if(song):
            song.played += 1
            song.save()
            data = {
                "message":"Played item is updated",
                "status":status.HTTP_200_OK,
                "played":song.played,
            }
            return Response(data = data)
    else:
        response = {
            "message":"Method not allowed",
            "status":status.HTTP_405_METHOD_NOT_ALLOWED,
        }
        return Response(data = response)


@api_view(["POST"])
@permission_classes([])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
@authentication_classes([SessionAuthentication , BasicAuthentication])
def updatelike(request , pk):
    if(request.method == "POST" and request.user.is_authenticated):
        try:
            song = get_object_or_404(Sound , pk=pk)
        except Sound.DoesNotExist:
            data = {
                "message":"Obejct Does not exist with this pk",
                "status":status.HTTP_400_BAD_REQUEST,

            }
            return Response(data = data)
        if(song):
            currentuser = UserProfile.objects.filter(user = request.user).first()
            if(currentuser):
                if(song in currentuser.songlike.all()):
                    currentuser.songlike.remove(song)
                    return Response(data = {"message":"You have already Like it " , "liked":False})
                else:
                    currentuser.songlike.add(song)
            song.like += 1
            song.save()
            data = {
                "message":"Like item is updated",
                "status":status.HTTP_200_OK,
                "like":song.like,
                "liked":True,
            }
            return Response(data = data)
    else:
        response = {
            "message":"Method not allowed or Please Login To Like The Song",
            "status":status.HTTP_405_METHOD_NOT_ALLOWED,
        }
        return Response(data = response)


class AlbumList(RetrieveAPIView):
    throttle_classes = [AnonRateThrottle , UserRateThrottle]
    model = Album
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    lookup_field = "category"
    permission_classes = []

    @method_decorator(cache_page(60*60*12))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
@api_view(["GET"])
@permission_classes([])
def mostplayedsong(request):
    if(request.method == "GET"):
        queryplay = Sound.objects.all().order_by("-played")[:20]
        querylike = Sound.objects.all().order_by("-like")[:20]
        print(querylike , queryplay)
        like = SoundSerializer(instance=querylike , many=True)
        played = SoundSerializer(instance=queryplay , many=True)
        data = {
            "played":played.data,
            "like":like.data
        }
        return Response(data = data)