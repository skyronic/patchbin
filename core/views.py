# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.core.urlresolvers import reverse
from core.forms import PatchForm
from core.models import Patch
import random

from diffviewer.patchutils import PatchToHtml

def index(request):
    """
    The Frontpage
    """
    template = loader.get_template('core/index.html')
    Form = PatchForm()
    context = Context({
        'patch_form':Form,
        'url_root': 'http://127.0.0.1:8000',
        'static_path':'http://127.0.0.1:8000/static'
        })
    return HttpResponse(template.render(context))

def submit(request):
    """
    Test the patch and save to database
    """
    errorMessage = ""
    newPatch = Patch()
    if(request.method == "POST"):
        if("patchText" in request.POST):
            newPatch.diffText = request.POST["patchText"]
            sampleChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            key = ''.join(random.sample(sampleChars, 6))
            newPatch.urlCode = key
            
            if(PatchToHtml(newPatch, newPatch.diffText)):
                pass
            else:
                errorMessage = "Parsing patch failed :("
            # TODO: Convert to HTML            
        else:
            errorMessage = "Expecting patchText POST parameter"
        if("patchDesc" in request.POST):
            newPatch.description = request.POST['patchDesc']

        if("authorName" in request.POST):
            newPatch.authorName = request.POST['authorName']
        
        if("emailAddress" in request.POST):
            newPatch.emailAddress = request.POST['emailAddress']
    else:
        errorMessage = "POST Requests only, please :)"
    
    if(errorMessage == ""): # No error        
        # Generate a primary key
        
        
        # Save to database
        newPatch.save()
        
        # Redirect
        return HttpResponseRedirect(reverse('patchbin.diffviewer.views.showpatch', args=(key,)))
            
    return HttpResponse(errorMessage)

def about(request):
    """Renders the about page"""
    template = loader.get_template('core/about.html')
    Form = PatchForm()
    context = Context({
        'url_root': 'http://127.0.0.1:8000',
        'static_path':'http://127.0.0.1:8000/static'
        })
    return HttpResponse(template.render(context))

def contribute(request):
    """Renders the /contribute/ page"""
    template = loader.get_template('core/contrib.html')
    Form = PatchForm()
    context = Context({
        'url_root': 'http://127.0.0.1:8000',
        'static_path':'http://127.0.0.1:8000/static'
        })
    return HttpResponse(template.render(context))

def sponsor(request):
    """Renders the /sponsor/ page"""
    template = loader.get_template('core/sponsor.html')
    Form = PatchForm()
    context = Context({
        'url_root': 'http://127.0.0.1:8000',
        'static_path':'http://127.0.0.1:8000/static'
        })
    return HttpResponse(template.render(context))
