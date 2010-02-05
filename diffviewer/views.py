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
    comments = []
    for individualChunk in chunks:
        # Process each chunk separately
        chunkComments = Comment.objects.filter(chunk=individualChunk)
        for comment in chunkComments:
            print comment.diffSide
            comments.append(comment)

    # Patch meta information
    patchDesc = "No description provided"
    patchAuthor = "No name provided"
    if (targetPatch.patchDesc != ""):
        patchDesc = targetPatch.patchDesc

    if (targetPatch.authorName != ""):
        patchAuthor = targetPatch.authorName



    context = Context({
        'chunks':chunks,
        'comments':comments,
        'url_root': 'http://127.0.0.1:8000',
        'static_path':'http://127.0.0.1:8000/static',
        'patchDesc':patchDesc,
        'patchAuthor':patchAuthor
    })
    return HttpResponse(template.render(context))

def javaScriptEscape(input):
    """Escapes string to make it javascript friendly"""
    input = input.replace('\'', '\\\'') # escape '
    input = input.replace('"', '\\"') # escape "
    input = input.replace('\n', '\\n') # change carriage return to
                                       # literal \n
    return input

def newcomment(request, urlCode):
    """Adds a new comment to the database"""
    output = "OK"
    debugvar = 0
    try:
        if(request.method == "POST"):
            name = request.POST["name"]
            name = javaScriptEscape(name)
            message = request.POST["message"]
            message = javaScriptEscape(message)
            side = request.POST["side"]
            side = javaScriptEscape(side)
            chunk = int(request.POST["chunk"])
            line = int(request.POST["line"])
            
            # basic sanity check
            if(not (side == 'lhs' or side == 'rhs')):
                output = "ERROR"
            else:
                targetPatch = get_object_or_404(Patch, pk=urlCode)
                print "patch - ", urlCode, " chunknum ", chunk
                targetChunks = Chunk.objects.filter(patch = targetPatch, chunkNum = chunk)
                print "Target chunks length - " + str(len(targetChunks))
                targetChunk = targetChunks[0]
                newComment = Comment()
                newComment.chunk = targetChunk
                newComment.commentAuthor = name
                newComment.commentText = message
                newComment.diffSide = side
                newComment.commentLine = line
                newComment.chunkID = chunk
                newComment.commentID = 0

                newComment.save()
        else:
            output = "ERROR"
    except Exception as e:
        from IPython import Shell
        Shell.IPShellEmbed()
        print "exception ", e
        output = "ERROR"
    return HttpResponse(output)
