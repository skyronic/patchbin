from django.db import models

# Create your models here.
class Patch(models.Model):
    urlCode = models.CharField(max_length=6, primary_key=True, db_column='urlcode')
    diffText = models.TextField()
    diffHTML = models.TextField()
    
    def __string__(self):
        return diffText