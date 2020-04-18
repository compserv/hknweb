from hknweb.candidate.models import Announcement, OffChallenge, BitByteActivity
import django
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

candidate = Group(name='candidate')
officer = Group(name='officer')
candidate.save()
officer.save()

def perm(name, codename, content):
	perm = Permission(name=name, codename=codename, content_type=content)
	perm.save()
	return perm

content = lambda app_label, model: ContentType.objects.get(app_label=app_label, model=model)

cand_permissions = {'view_announcement':('Announcement', 'candidate'), \
			   'add_offchallenge':('OffChallenge', 'candidate'), \
			   'view_offchallenge':('OffChallenge', 'candidate'), \
			   'change_offchallenge':('OffChallenge', 'candidate'), \
			   'add_bitbyteactivity':('BitByteActivity','candidate'), \
     		   'view_user':('user','auth'), \
     		   'view_event':('Event','events'), \
     		   'add_rsvp':('Rsvp','events'), \
     		   'remove_rsvp':('Rsvp','events')}
off_permissions = cand_permissions
off_permissions['add_event'] = ('Event', 'events')
off_permissions['change_event'] = ('Event', 'events')

candidate.permissions = [perm(p, p, content(cand_permissions[p][1],cand_permissions[p][0])) for p in cand_permissions.keys()]
officer.permissions = [perm(p, p, content(off_permissions[p][1],off_permissions[p][0])) for p in cand_permissions.keys()]
