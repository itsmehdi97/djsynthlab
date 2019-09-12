# from django.db.models.signals import post_save, Signal
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import Profile

# print('hi im here')

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     print('befor created')
#     if created:
#         print(kwargs)
#         print('profile created')
#         #Profile.objects.create(user=instance)
