# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
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

            secret = ''.join(random.sample(sampleChars, 16))
            newPatch.secretKey = secret
            
            if(PatchToHtml(newPatch, newPatch.diffText)):
                pass
            else:
                errorMessage = "Parsing patch failed :("
            # TODO: Convert to HTML            
        else:
            errorMessage = "Expecting patchText POST parameter"
        if("description" in request.POST):
            newPatch.patchDesc = request.POST['description']
        else:
            newPatch.patchDesc = ""
        
        if("emailAddress" in request.POST):
            if(request.POST['emqilAddress'] != ""):
                newPatch.authorEmail = request.POST['emailAddress']

        if("emailNotify" in request.POST):
            newPatch.emailNotify = 0
        else:
            newPatch.emailNotify = 0
    else:
        errorMessage = "POST Requests only, please :)"
    
    if(errorMessage == ""): # No error        
        # Save to database
        newPatch.authorName = 'andy'
        newPatch.save()

        # Make an email to send out
        if(newPatch.authorEmail):
            subject = 'New Patchbin patch!'
            message = """
            Hi!

            Thanks for using patchbin!

            You can view and share your patch with the URL:
                ##PATCH_URL##

            To delete your patch, visit:
                ##PATCH_DELETE##

            In the event you want to delete any comment, use this link to moderate:
                ##PATCH_COMMENT##

            Thanks!
            Patchbot P-)
            """
            # Do not send a mail right now
            
        # Redirect
        return HttpResponseRedirect(reverse('patchbin.diffviewer.views.showpatch', args=(key,)))
            
    return HttpResponse(errorMessage)


