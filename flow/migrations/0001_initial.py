
from south.db import db
from django.db import models
from Learness.flow.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Comment'
        db.create_table('flow_comment', (
            ('id', orm['flow.Comment:id']),
            ('comment', orm['flow.Comment:comment']),
            ('commenttoanswer', orm['flow.Comment:commenttoanswer']),
            ('commenttoquestion', orm['flow.Comment:commenttoquestion']),
        ))
        db.send_create_signal('flow', ['Comment'])
        
        # Adding model 'Question'
        db.create_table('flow_question', (
            ('id', orm['flow.Question:id']),
            ('title', orm['flow.Question:title']),
            ('explanation', orm['flow.Question:explanation']),
            ('relatedProject', orm['flow.Question:relatedProject']),
            ('datecreated', orm['flow.Question:datecreated']),
            ('datemodified', orm['flow.Question:datemodified']),
            ('answered', orm['flow.Question:answered']),
            ('tags', orm['flow.Question:tags']),
        ))
        db.send_create_signal('flow', ['Question'])
        
        # Adding model 'Link'
        db.create_table('flow_link', (
            ('id', orm['flow.Link:id']),
            ('link', orm['flow.Link:link']),
            ('commentlink', orm['flow.Link:commentlink']),
            ('answerlink', orm['flow.Link:answerlink']),
            ('questionlink', orm['flow.Link:questionlink']),
        ))
        db.send_create_signal('flow', ['Link'])
        
        # Adding model 'Project'
        db.create_table('flow_project', (
            ('id', orm['flow.Project:id']),
            ('name', orm['flow.Project:name']),
            ('owner', orm['flow.Project:owner']),
            ('tags', orm['flow.Project:tags']),
        ))
        db.send_create_signal('flow', ['Project'])
        
        # Adding model 'Answer'
        db.create_table('flow_answer', (
            ('id', orm['flow.Answer:id']),
            ('explanation', orm['flow.Answer:explanation']),
            ('question', orm['flow.Answer:question']),
            ('tags', orm['flow.Answer:tags']),
        ))
        db.send_create_signal('flow', ['Answer'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Comment'
        db.delete_table('flow_comment')
        
        # Deleting model 'Question'
        db.delete_table('flow_question')
        
        # Deleting model 'Link'
        db.delete_table('flow_link')
        
        # Deleting model 'Project'
        db.delete_table('flow_project')
        
        # Deleting model 'Answer'
        db.delete_table('flow_answer')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'flow.answer': {
            'explanation': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flow.Question']"}),
            'tags': ('tagging.fields.TagField', [], {})
        },
        'flow.comment': {
            'comment': ('django.db.models.fields.TextField', [], {}),
            'commenttoanswer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flow.Answer']"}),
            'commenttoquestion': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flow.Question']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'flow.link': {
            'answerlink': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flow.Answer']"}),
            'commentlink': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flow.Comment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'questionlink': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flow.Question']"})
        },
        'flow.project': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'tags': ('tagging.fields.TagField', [], {})
        },
        'flow.question': {
            'answered': ('django.db.models.fields.CharField', [], {'default': "'p'", 'max_length': '1'}),
            'datecreated': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'datemodified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'explanation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'relatedProject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flow.Project']"}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }
    
    complete_apps = ['flow']
