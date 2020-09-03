from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Contact(models.Model):
    user_form = models.ForeignKey('auth.User',related_name='rel_from_set',on_delete=models.CASCADE) # foreignkey for the user that creates the relationship
    user_to = models.ForeignKey('auth.User',related_name='rel_to_set',on_delete=models.CASCADE) # foreignkey for the user being followed
    created = models.DateTimeField(auto_now_add=True,db_index=True)  # to store the time when the relationship was created,we use db_index=True to create a database index for the created field.This will improve query performance when ordering querysets by this field

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_form,self.user_to)
