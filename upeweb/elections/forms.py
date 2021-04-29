from django import forms
from upeweb.models import User, Group
# from django.contrib.auth.models import Group

class OfficerForm(forms.Form):
    # Execs
    execPresident = forms.ModelChoiceField(label = 'Presidenttest', queryset=User.objects.all())
    execVicePresident = forms.ModelChoiceField(label = 'Vice President', queryset=User.objects.all())
    execRecordingSecretary = forms.ModelChoiceField(label = 'Recording Secretary', queryset=User.objects.all())
    execCorrespondingSecretary = forms.ModelChoiceField(label = 'Corresponding Secretary', queryset=User.objects.all())
    execTreasurer = forms.ModelChoiceField(label = 'Treasurer', queryset=User.objects.all())
    execDepartmentRelations = forms.ModelChoiceField(label = 'Department Relations', queryset=User.objects.all())
    execAluminiRelations = forms.ModelChoiceField(label = 'Alumini Relations', queryset=User.objects.all())

    #Activites Committee
    actOfficer = forms.ModelMultipleChoiceField(label = 'Activites Officer', queryset=User.objects.all())
    actAssistantOfficer = forms.ModelMultipleChoiceField(label = 'Activites Assistant Officer', required=False, queryset=User.objects.all())

    #Bridge Committee
    bridgeOfficer = forms.ModelMultipleChoiceField(label = 'Bridge Officer', queryset=User.objects.all())
    bridgeAssistantOfficer = forms.ModelMultipleChoiceField(label = 'Bridge Assistant Officer', required=False, queryset=User.objects.all())

    #Computing Services Committee
    compservOfficer = forms.ModelMultipleChoiceField(label = 'Compserv Officer', queryset=User.objects.all())
    compservAssistantOfficer = forms.ModelMultipleChoiceField(label = 'Compserv Assistant Officer', required=False, queryset=User.objects.all())

    #Decal Committee
    decalOfficer = forms.ModelMultipleChoiceField(label = 'Decal Officer', queryset=User.objects.all())
    decalAssistantOfficer = forms.ModelMultipleChoiceField(label = 'Decal Assistant Officer', required=False, queryset=User.objects.all())

    #Industrial Relations Committee
    indrelOfficer = forms.ModelMultipleChoiceField(label = 'Indrel Officer', queryset=User.objects.all())
    indrelAssistantOfficer = forms.ModelMultipleChoiceField(label = 'Indrel Assistant Officer', required=False, queryset=User.objects.all())

    #Service Committee
    servOfficer = forms.ModelMultipleChoiceField(label = 'Service Officer', queryset=User.objects.all())
    servAssistantOfficer = forms.ModelMultipleChoiceField(label = 'Service Assistant Officer', required=False, queryset=User.objects.all())

    #Student Relations Committee
    studrelOfficer = forms.ModelMultipleChoiceField(label = 'Studrel Officer', queryset=User.objects.all())
    studrelAssistantOfficer = forms.ModelMultipleChoiceField(label = 'Studrel Assistant Officer', required=False, queryset=User.objects.all())

    #Tutoring Committee
    tutorOfficer = forms.ModelMultipleChoiceField(label = 'Tutoring Officer', queryset=User.objects.all())
    tutorAssistantOfficer = forms.ModelMultipleChoiceField(label = 'Tutoring Assistant Officer', required=False, queryset=User.objects.all())

    def assignGroups(self):
        # General Officers
        g = Group.objects.get(name='officers')
        for x in self.cleaned_data.values():
            if x != '':
                g.user_set.add(User.objects.get(username=x))

        ''' Specfic Permissions
        execs = Group.objects.get(name = 'executives')
        act = Group.objects.get(name = 'activites')
        bridge = Group.objects.get(name = 'bridge')
        compserv = Group.objects.get(name = 'compserv')
        decal = Group.objects.get(name = 'decal')
        indrel = Group.objects.get(name = 'indrel')
        serv = Group.object.get(name = 'service')
        studrel = Group.object.get(name = 'studrel')
        tutoring = Group.object.get(name = 'tutoring')
        off = Group.objects.get(name='officers')

        for pos, user in self.cleaned_data:
            if user != '':
                if 'exec' in pos:
                    execs.user_set.add(User.objects.get(username=user))
                else if 'act' in pos:
                    act.user_set.add(User.objects.get(username=user))
                else if 'bridge' in pos:
                    bridge.user_set.add(User.objects.get(username=user))
                else if 'compserv' in pos:
                    compserv.user_set.add(User.objects.get(username=user))
                else if 'decal' in pos:
                    decal.user_set.add(User.objects.get(username=user))
                else if 'indrel' in pos:
                    indrel.user_set.add(User.objects.get(username=user))
                else if 'serv' in pos:
                    serv.user_set.add(User.objects.get(username=user))
                else if 'studrel' in pos:
                    studrel.user_set.add(User.objects.get(username=user))
                else if 'tutoring' in pos:
                    tutoring.user_set.add(User.objects.get(username=user))
                else:
                    off.user_set.add(User.objects.get(username=user))
        '''
