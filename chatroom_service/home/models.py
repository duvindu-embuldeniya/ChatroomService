from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    email = models.EmailField(null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def save(self, *args, **kwargs):
        # Check if the profile already exists
        if self.pk:
            old_profile = Profile.objects.get(pk=self.pk)
            old_image = old_profile.image if old_profile.image else None
        else:
            old_image = None

        super(Profile, self).save(*args, **kwargs)

        #New image uploaded, delete the old one
        if self.image and self.image != old_image:
            if old_image:
                try:
                    if os.path.isfile(old_image.path):
                        os.remove(old_image.path)
                except Exception as e:
                    print(f"Error deleting old image: {e}")

        #Image removed, delete the current image
        elif not self.image and old_image:
            try:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)
            except Exception as e:
                print(f"Error deleting current image: {e}")

        # Resize 
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
            img.close()

class Topic(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
    


class Rooms(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name  = models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        ordering = ['-created']



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.body[:50]}"

    class Meta:
        ordering = ['-created']