# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.core.urlresolvers import reverse
from core.forms import PatchForm
from core.models import Patch
import random
import settings

from diffviewer.patchutils import PatchToHtml

def index(request):
    """
    The Frontpage
    """
    template = loader.get_template('core/index.html')
    Form = PatchForm()
    context = Context({
        'patch_form':Form,
        'url_root': settings.DOMAIN,
        'static_path':settings.DOMAIN + '/static'
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
                errorMessage = """Parsing patch failed :(. Unified Diff format
                only please. Thanks! If you feel that this is an error, please
                email anirudh@anirudhsanjeev.org with the patch attached"""
            # TODO: Convert to HTML            
        else:
            errorMessage = "Expecting patchText POST parameter"
        if("patchDesc" in request.POST):
            newPatch.patchDesc = request.POST['patchDesc']
            newPatch.patchDesc.replace('\n\n', '<br><br>')

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
        'url_root': settings.DOMAIN,
        'static_path':settings.DOMAIN + '/static'
        })
    return HttpResponse(template.render(context))

def contribute(request):
    """Renders the /contribute/ page"""
    template = loader.get_template('core/contrib.html')
    Form = PatchForm()
    context = Context({
        'url_root': settings.DOMAIN,
        'static_path':settings.DOMAIN + '/static'
        })
    return HttpResponse(template.render(context))

def sponsor(request):
    """Renders the /sponsor/ page"""
    template = loader.get_template('core/sponsor.html')
    Form = PatchForm()
    context = Context({
        'url_root': settings.DOMAIN,
        'static_path':settings.DOMAIN + '/static'
        })
    return HttpResponse(template.render(context))
