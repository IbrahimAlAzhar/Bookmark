from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image  # use the Image model and use these fields
        fields = ('title', 'url', 'description') # users will not enter the image URL directly in the form,we will provide them with a javascript tool choose an image from an external site and our form will receive it URL as a parameter
        widgets = {
            'url': forms.HiddenInput, # this widget because we don't want this field to be visible
        }

    def clean_url(self):
        url = self.cleaned_data['url']  # get the value of url field accessing cleaned_data dict. of the form instance
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower() # take extension of image,split the right side and take the extension(first element)
        if extension not in valid_extensions: # check the extension is jpg or jpeg format otherwise raise error
            raise forms.ValidationError('The given URL does not '\
                                        'match valid image extensions.')
        return url

    def save(self, force_insert=False, force_update=False, commit=True): # override the save method for saving purpose,if commit=False then save() method will return a model instance but will not save it to the database
        image = super(ImageCreateForm, self).save(commit=False) # create a new image instance from ImageCreateForm class and commit=False means don't save it to database
        image_url = self.cleaned_data['url']  # we get the url from the cleaned_data dict. of the form
        # generated the image name by combining the image title slug with the original file extension(jpg or jpeg)
        image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.', 1)[1].lower())

        # download image from the given URL,use the python urllib module to download the image and
        response = request.urlopen(image_url)
        # passing it a contentfile object that is instantiated with the download file
        image.image.save(image_name, ContentFile(response.read()), save=False) # call the save() method of the image field,passing it a ContentFile obj that is instantiated with the downloaded file content. save = false means avoid the save in database yet
        if commit:  # now if the commit is true then save the image
            image.save()
        return image
