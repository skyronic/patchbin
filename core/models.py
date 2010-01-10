from django.db import models

# Create your models here.
class Patch(models.Model):
    urlCode = models.CharField(max_length=6, primary_key=True, db_column='urlcode')
    diffText = models.TextField()
    diffHTML = models.TextField()
    
class Chunk(models.Model):
    patch = models.ForeignKey(Patch)
    originalFile = models.CharField(max_length = 50)
    newFile = models.CharField(max_length = 50)
    chunkText = models.TextField()
    chunkHtml = models.TextField()
    
class Comment(models.Model):
    chunk = models.ForeignKey(Chunk)
    commentText = models.TextField()
    commentLine = models.IntegerField()