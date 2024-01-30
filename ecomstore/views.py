from django.shortcuts import render 
from django.template import RequestContext 
def file_not_found_404(request,exception): 
 page_title = 'Page Not Found' 
 return render('404.html', locals(), context_instance=RequestContext(request)) 