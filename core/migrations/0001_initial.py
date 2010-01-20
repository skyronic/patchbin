
from south.db import db
from django.db import models
from patchbin.core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Comment'
        db.create_table('core_comment', (
            ('id', orm['core.Comment:id']),
            ('chunk', orm['core.Comment:chunk']),
            ('chunkID', orm['core.Comment:chunkID']),
            ('commentID', orm['core.Comment:commentID']),
            ('commentAuthor', orm['core.Comment:commentAuthor']),
            ('commentText', orm['core.Comment:commentText']),
            ('commentLine', orm['core.Comment:commentLine']),
            ('diffSide', orm['core.Comment:diffSide']),
        ))
        db.send_create_signal('core', ['Comment'])
        
        # Adding model 'Chunk'
        db.create_table('core_chunk', (
            ('id', orm['core.Chunk:id']),
            ('patch', orm['core.Chunk:patch']),
            ('chunkNum', orm['core.Chunk:chunkNum']),
            ('originalFile', orm['core.Chunk:originalFile']),
            ('newFile', orm['core.Chunk:newFile']),
            ('chunkText', orm['core.Chunk:chunkText']),
            ('chunkHtml', orm['core.Chunk:chunkHtml']),
        ))
        db.send_create_signal('core', ['Chunk'])
        
        # Adding model 'Patch'
        db.create_table('core_patch', (
            ('urlCode', orm['core.Patch:urlCode']),
            ('diffText', orm['core.Patch:diffText']),
            ('diffHTML', orm['core.Patch:diffHTML']),
        ))
        db.send_create_signal('core', ['Patch'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Comment'
        db.delete_table('core_comment')
        
        # Deleting model 'Chunk'
        db.delete_table('core_chunk')
        
        # Deleting model 'Patch'
        db.delete_table('core_patch')
        
    
    
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
            'diffHTML': ('django.db.models.fields.TextField', [], {}),
            'diffText': ('django.db.models.fields.TextField', [], {}),
            'urlCode': ('django.db.models.fields.CharField', [], {'max_length': '6', 'primary_key': 'True', 'db_column': "'urlcode'"})
        }
    }
    
    complete_apps = ['core']
