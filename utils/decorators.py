from django.http import HttpResponse
from django.shortcuts import redirect

#when we apply a decorator to a funcction that function is passed in the decorator function as an argument this is done to add some additional functionality to the function
#if we apply this decorator to loginPage of our views.py loginPage becomes view_func so this function doesnt get exceuted until and unless we perform the checks and additional functionalities of the wrapper function
def unauthenticated_user(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('CustomerManage')
        else:
            return view_func(request,*args, **kwargs) # we exceute the parent function in case user is not authenticated  
    return wrapper_func

def allowed_user(allowed_roles=[]):
    def decorators(view_func):
        def wrapper_func(request,*args,**kwargs):
            group=None
        
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
                
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("You are not authorised to view this section")            
        return wrapper_func
    return decorators

def admin_only(view_func):
    def wrapper_function(request,*args,**kwargs):
        group =None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=='customer':
            return redirect('user-page')
        if group=='admin':
            return view_func(request,*args,**kwargs)
    return wrapper_function


