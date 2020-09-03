from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    # foreign key because a user can post multiple images
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200,blank=True) # for making beautiful SEO-friendly URLs
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,db_index=True) # this datetime is automatically set when the object is created,we use db_index=True so that django creates an index in the database for this field
    # this many to many relationship because a user like multiple images and a images liked by multiple users
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, # add another field to the image model to store the users who like an image,use many to many relationship because a user might like multiple images and each image can be liked by multiple users
                                        related_name='images_liked',
                                        blank=True) # we use 'image.users_like.all() for all user in one image or 'users.images_liked.all()' for all images liked by a user where 'images_liked' is related name

    def __str__(self):
        return self.title

    def get_absolute_url(self): # this method use for detail view,the url for detail image needs the parameter id,slug
        return reverse('images:detail',args=[self.id,self.slug]) # using args so passing a list,if you use kwargs then you have to pass a dictionary

    def save(self, *args, **kwargs):
        # to automatically generate the slug field based on the value of the title field when no slug is provided
        # slugify function provided to automatically generate the image slug so that users don't have to manually enter a slug for each image
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image,self).save(*args, **kwargs)

