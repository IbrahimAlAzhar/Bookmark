from django.http import HttpResponseBadRequest


# here we create a custom decorator which one we use in views.py file
def ajax_required(f): # this code is our custom ajax_required decorator,it defines a wrap function that returns an HttpResponseBadRequest object(HTTP 400 code) if the request is not AJAX,otherwise it returns the decorated function
    def wrap(request,*args,**kwargs):
        if not request.is_ajax():  # if the request in not ajax then return the HttpresponseBadRequest otherwise returns the decorated function and lastly it return wrap which includes doc and name
            return HttpResponseBadRequest()
        return f(request,*args,**kwargs) # if the request is ajax then it returns the request with args and kwargs
    wrap.__doc__ = f.__doc__  # if the request is ajax or not the 'doc' in 'doc' and 'name' in f store it to wrap and return it
    wrap.__name__ = f.__name__
    return wrap
