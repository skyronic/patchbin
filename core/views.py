# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.core.urlresolvers import reverse
from core.forms import PatchForm
from core.models import Patch
import random

def index(request):
    """
    The Frontpage
    """
    template = loader.get_template('core/index.html')
    Form = PatchForm()
    context = Context({
        'patch_form':Form,
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
            
            # TODO: Convert to HTML            
        else:
            errorMessage = "Expecting patchText POST parameter"
        if("description" in request.POST):
            newPatch.description = request.POST['description']
        
        if("emailAddress" in request.POST):
            newPatch.emailAddress = request.POST['emailAddress']
    else:
        errorMessage = "POST Requests only, please :)"
    
    if(errorMessage == ""): # No error        
        # Generate a primary key
        sampleChars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        key = ''.join(random.sample(sampleChars, 6))
        newPatch.urlCode = key
        
        # Save to database
        newPatch.save()
        
        # Redirect
        return HttpResponseRedirect(reverse('patchbin.core.views.showpatch', args=(key,)))
            
    return HttpResponse(errorMessage)

def showpatch(request, urlCode):
    """
    Shows the patch
    """
    patch = get_object_or_404(Patch, pk=urlCode)
    template = loader.get_template('core/showpatch.html')
    context = Context({
        'patchText' : patch.diffText,
        })
    return HttpResponse(template.render(context))