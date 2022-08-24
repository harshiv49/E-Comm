from django.shortcuts import render
from blog.models import Blog 
from django.core.paginator import Paginator
# Create your views here.
def blog(request):
    # blogs=Blog.objects.all()
    # print(blogs)
    p = Paginator(Blog.objects.all(), 3)
    page= request.GET.get('page')
    blog = p.get_page(page)
    #hack to get around
    
    context={'blogs':blog}
    return render(request,"blog/blog.html",context)