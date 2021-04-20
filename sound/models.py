import sys
from django.db import models
import datetime
from .utils import randomString
from tagging.fields import TagField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.



def upload_path_image(instance , filename):
    return 'upload/image/{0}-{1}/{2}'.format(randomString(),datetime.date.today() , filename)


def upload_path_sound(instance , filename):
    return 'upload/sound/{0}-{1}/{2}'.format(randomString(),datetime.date.today() , filename)

class Sound(models.Model):
    name = models.CharField(null=False , blank=False , max_length=300)
    song_image = models.ImageField(null = False , blank = False , upload_to=upload_path_image)
    song_name = models.FileField(null=False , blank=False , upload_to=upload_path_sound)
    like = models.IntegerField(default=0)
    played = models.IntegerField(default=0)
    tag = TagField()
    singer = models.CharField(max_length=100, null=True , blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def compressImage(self):
        imageTemproary = Image.open(self.song_image)
        outputIoStream = BytesIO()
        if(imageTemproary.height > 150 or imageTemproary.width > 200):
            imageTemproary = imageTemproary.resize((100,100) , Image.ANTIALIAS)
            imageTemproary.save(outputIoStream , format='JPEG', quality=90)
            outputIoStream.seek(0)
            self.song_image = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % self.song_image.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
            print("Image size has been updated")


    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self.name)

    class Meta:
        ordering = ["played"]
    

    def save(self , *args , **kwargs):
        self.compressImage()
        
        super(Sound,self).save(*args , **kwargs)



CATEGORY_CHOICES = [
    ("PUN" , "PUNJABI"),
    ("ENG" , "ENGLISH"),
    ("HIN" , "HINDI"),
    ("DEV" , "BHAKTI"),
]


class Album(models.Model):
    sound = models.ManyToManyField(Sound)
    name = models.CharField(max_length=200)
    datepublish = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES , default="HIN")


    def __str__(self):
        return self.name    

    def __repr__(self):
        return self.name









        
        

    
