from hknweb.candidate.models import Announcement, OffChallenge, BitByteActivity
from hknweb.events.models import Event, Rsvp
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

candidate = Group.objects.get_or_create(name='candidate')[0]
officer = Group.objects.get_or_create(name='officer')[0]

#CANDIDATE AND OFFICER PERMISSIONS
announcement = ('view_announcement', Announcement)
add_offchallenge = ('add_offchallenge', OffChallenge)
view_offchallenge =	('view_offchallenge', OffChallenge)
change_offchallenge = ('change_offchallenge', OffChallenge)
add_bitbyteactivity = ('add_bitbyteactivity', BitByteActivity)
view_event = ('view_event', Event)
add_rsvp = ('add_rsvp',Rsvp)
remove_rsvp = ('remove_rsvp',Rsvp)
view_user = ('view_user', User)

cand_permission_names = [announcement, add_offchallenge, view_offchallenge, \
	change_offchallenge, add_bitbyteactivity, add_rsvp, remove_rsvp, view_user]

# OFFICER ONLY PERMISSIONS
add_event = ('add_event', Event)
change_event = ('change_event', Event)

off_permission_names = [add_event, change_event]

# SETTING PERMISSIONS TO GROUPS
cand_permissions = []
for perm in cand_permission_names:
	ct =  ContentType.objects.get_for_model(perm[1])
	permission = Permission.objects.get(codename=perm[0], content_type=ct)
	cand_permissions.append(permission)

candidate.permissions.set(cand_permissions)
officer.permissions.set(cand_permissions)

for perm in off_permission_names:
	ct =  ContentType.objects.get_for_model(perm[1])
	permission = Permission.objects.get(codename=perm[0], content_type=ct)
	officer.permissions.add(permission)


