from .models import Sound , Album
from rest_framework import serializers

class SoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = ["name" , "song_image" , "pk" , "like" , "played" , "tag" , "singer" , "upload_date"]
        
        
class SoundDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    sound = serializers.SerializerMethodField()
    class Meta:
        model = Album
        fields = ["name" , "datepublish" , "category" , "sound"]
        depth = 1

    def get_sound(self  , obj):
        print("WORKING")
        return SoundSerializer(instance=obj.sound , many=True).data


