from django.contrib.auth.models import Permission, User
from django.db import models
from django.contrib.admin import widgets
from django.db.models.signals import post_save
from django.dispatch import receiver

#
# class Author(models.Model):
#     user = models.OneToOneField(User,unique=True)
#     email = models.EmailField(blank=True)
#     phone = models.BigIntegerField(blank=True)
#
#     @receiver(post_save, sender=User)
#     def create_user_profile(sender,instance,created,**kwargs):
#         if created:
#             Author.objects.create(user=instance)
#
#     @receiver(post_save,sender=User)
#     def save_profile(sender,instance,**kwargs):
#         instance.author.save()
#
#
#     def __str__(self):
#         return self.user
#


class Note(models.Model):
    user = models.ForeignKey(User,default=1)
   # artist = models.CharField(max_length=250)
    title = models.CharField(max_length=500)
    create_date = models.DateTimeField(auto_now_add=True)
    reminder_date = models.DateField()
    #album_logo = models.FileField()
    is_important = models.BooleanField(default=False)


    def __str__(self):
        return str(self.user) + ' - ' + str(self.title)


class List(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    item = models.CharField(max_length=250)
    is_important = models.BooleanField(default=False)

    def __str__(self):
        return self.item
