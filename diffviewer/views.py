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