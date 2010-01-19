# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import Context, loader
from django.core.urlresolvers import reverse
from core.forms import PatchForm
from core.models import Patch, Chunk, Comment
import random


def showpatch(request, urlCode):
    """
    Shows the patch
    """
    targetPatch = get_object_or_404(Patch, pk=urlCode)
    
    # Get all the chunks for this patch
    chunks = Chunk.objects.filter(patch = targetPatch)   
    
    template = loader.get_template('diffviewer/showpatch.html')
    context = Context({
        'chunks':chunks,
        })
    return HttpResponse(template.render(context))


def newcomment(request, urlCode):
    """Adds a new comment to the database"""
    output = "OK"
    if(request.method == "POST"):
        name = request.POST["name"]
        message = request.POST["message"]
        print "Recieved a request: " + name + message
    else:
        output = "ERROR"

    return HttpResponse(output)
