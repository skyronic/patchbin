
from south.db import db
from django.db import models
from patchbin.core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Patch.patchDesc'
        db.add_column('core_patch', 'patchDesc', orm['core.patch:patchDesc'])
        
        # Adding field 'Patch.authorEmail'
        db.add_column('core_patch', 'authorEmail', orm['core.patch:authorEmail'])
        
        # Adding field 'Patch.secretKey'
        db.add_column('core_patch', 'secretKey', orm['core.patch:secretKey'])
        
        # Adding field 'Patch.authorName'
        db.add_column('core_patch', 'authorName', orm['core.patch:authorName'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Patch.patchDesc'
        db.delete_column('core_patch', 'patchDesc')
        
        # Deleting field 'Patch.authorEmail'
        db.delete_column('core_patch', 'authorEmail')
        
        # Deleting field 'Patch.secretKey'
        db.delete_column('core_patch', 'secretKey')
        
        # Deleting field 'Patch.authorName'
        db.delete_column('core_patch', 'authorName')
        
    
    
    models = {
        'core.chunk': {
            'chunkHtml': ('django.db.models.fields.TextField', [], {}),
            'chunkNum': ('django.db.models.fields.IntegerField', [], {}),
            'chunkText': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newFile': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'originalFile': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'patch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Patch']"})
        },
        'core.comment': {
            'chunk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Chunk']"}),
            'chunkID': ('django.db.models.fields.IntegerField', [], {}),
            'commentAuthor': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'commentID': ('django.db.models.fields.IntegerField', [], {}),
            'commentLine': ('django.db.models.fields.IntegerField', [], {}),
            'commentText': ('django.db.models.fields.TextField', [], {}),
            'diffSide': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'core.patch': {
            'authorEmail': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'authorName': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'diffHTML': ('django.db.models.fields.TextField', [], {}),
            'diffText': ('django.db.models.fields.TextField', [], {}),
            'patchDesc': ('django.db.models.fields.TextField', [], {}),
            'secretKey': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'urlCode': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True', 'db_column': "'urlcode'"})
        }
    }
    
    complete_apps = ['core']
