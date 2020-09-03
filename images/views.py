from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def image_list(request):
    images = Image.objects.all() # we create a Queryset to return all images from the database
    paginator = Paginator(images,8) # we build a paginator object to paginate the results retrieving 8 images per page
    page = request.GET.get('page') # take the current page number
    try:
        images = paginator.page(page) # take the all images in current page and store it to 'images' variable
    except PageNotAnInteger:
        # if image is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage: # we get an empty page exception if the requested page is out of range.If this is the case and requested is done via AJAX,we return an empty Httpresponse that will help us stop the AJAX pagination on the client side
        if request.is_ajax():
            # if the request is AJAX and the page is out of range,return an empty page
            return HttpResponse('')
        # if page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,'images/image/list_ajax.html',{'section':'images','images':images}) # for ajax requests,we render the list_ajax.html template,this template will only contain the images of the requested page
    return render(request,'images/image/list.html',{'section':'images','images':images}) # (else) we render the list.html template,this template will extend the base.html to display the whole page and will include the list_ajax.html template to include the list of images


@login_required # using this decorator to prevent access for unauthenticated users
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False) # create a instance of form class and store it to new_item variable,and don't save it to database yet
            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url()) # redirect the user to the canonical URL of new image
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug): # take the parameter id,slug from urls
    image = get_object_or_404(Image,id=id,slug=slug) # find the current image using the parameter id,slug
    return render(request,'images/image/detail.html',{'section':'images','image':image})


@ajax_required # ajax required is custom file which one we create on common/decorators.py file which requires the ajax to see the 'image_like' function
@login_required  # the decorator prevents users that are not logged in from accessing this view
@require_POST  # this decorator returns an HttpResponseNotAllowed object,if the HTTP request is not done via POST,this way we only allow POST requests for this view
def image_like(request):
    image_id = request.POST.get('id') # the ID of the image object on which the user is performing the action
    action = request.POST.get('action')  # the action that the user wants to perform,which we assume to be a string with the value like or unlike
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user) # add the current user of 'Image' model in 'users_like' attribute,using add() or remove() methods
            else:
                image.users_like.remove(request.user) # remove the current user of 'Image' model in 'users like' attribute(using fk relationship)
            return JsonResponse({'status':'ok'})

        except:
            pass
    return JsonResponse({'status':'ko'}) # it is HTTP response with json content type,converting the given object into a JSON output

