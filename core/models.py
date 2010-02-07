from django.db import models

# Create your models here.
class Patch(models.Model):
    urlCode = models.CharField(max_length=6, primary_key=True, db_column='urlcode')
    diffText = models.TextField()
    diffHTML = models.TextField()
    authorName = models.CharField(max_length=50)
    authorEmail = models.CharField(max_length=50)
    patchDesc = models.TextField()
    secretKey = models.CharField(max_length = 16)
    
class Chunk(models.Model):
    patch = models.ForeignKey(Patch)
    chunkNum = models.IntegerField()
    originalFile = models.CharField(max_length = 100)
    newFile = models.CharField(max_length = 100)
    chunkText = models.TextField()
    chunkHtml = models.TextField()
    
class Comment(models.Model):
    chunk = models.ForeignKey(Chunk)
    chunkID = models.IntegerField() # we can just use chunk.chunkNum
    # But this seems to be more efficient
    commentID = models.IntegerField()
    commentAuthor = models.CharField(max_length = 30)
    commentText = models.TextField()
    commentLine = models.IntegerField()
    diffSide = models.CharField(max_length = 5)
