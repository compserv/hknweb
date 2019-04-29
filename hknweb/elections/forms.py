from django import forms
from hknweb.models import User, Group
# from django.contrib.auth.models import Group

class OfficerForm(forms.Form):
    # Execs
    execPresident = forms.ModelMultipleChoiceField(label = 'Presidenttest', queryset=User.objects.all())
    execVicePresident = forms.ModelMultipleChoiceField(label = 'Vice President', queryset=User.objects.all())
    execRecordingSecretary = forms.ModelMultipleChoiceField(label = 'Recording Secretary', queryset=User.objects.all())
    execCorrespondingSecretary = forms.ModelMultipleChoiceField(label = 'Corresponding Secretary', queryset=User.objects.all())
    execTreasurer = forms.ModelMultipleChoiceField(label = 'Treasurer', queryset=User.objects.all())
    execDepartmentRelations = forms.ModelMultipleChoiceField(label = 'Department Relations', queryset=User.objects.all())
    execAluminiRelations = forms.ModelMultipleChoiceField(label = 'Alumini Relations', queryset=User.objects.all())

    #Activites Committee
    actOfficer1 = forms.ModelMultipleChoiceField(label = 'Activites Officer', queryset=User.objects.all())
    actOfficer2 = forms.ModelMultipleChoiceField(label = 'Activites Officer', required=False, queryset=User.objects.all())
    actOfficer3 = forms.ModelMultipleChoiceField(label = 'Activites Officer', required=False, queryset=User.objects.all())
    actOfficer4 = forms.ModelMultipleChoiceField(label = 'Activites Officer', required=False, queryset=User.objects.all())
    actOfficer5 = forms.ModelMultipleChoiceField(label = 'Activites Officer', required=False, queryset=User.objects.all())
    actOfficer6 = forms.ModelMultipleChoiceField(label = 'Activites Officer', required=False, queryset=User.objects.all())
    actAssistantOfficer1 = forms.ModelMultipleChoiceField(label = 'Activites Assistant Officer', required=False, queryset=User.objects.all())
    actAssistantOfficer2 = forms.ModelMultipleChoiceField(label = 'Activites Assistant Officer', required=False, queryset=User.objects.all())
    actAssistantOfficer3 = forms.ModelMultipleChoiceField(label = 'Activites Assistant Officer', required=False, queryset=User.objects.all())

    #Bridge Committee
    bridgeOfficer1 = forms.ModelMultipleChoiceField(label = 'Bridge Officer', queryset=User.objects.all())
    bridgeOfficer2 = forms.ModelMultipleChoiceField(label = 'Bridge Officer', required=False, queryset=User.objects.all())
    bridgeOfficer3 = forms.ModelMultipleChoiceField(label = 'Bridge Officer', required=False, queryset=User.objects.all())
    bridgeOfficer4 = forms.ModelMultipleChoiceField(label = 'Bridge Officer', required=False, queryset=User.objects.all())
    bridgeOfficer5 = forms.ModelMultipleChoiceField(label = 'Bridge Officer', required=False, queryset=User.objects.all())
    bridgeOfficer6 = forms.ModelMultipleChoiceField(label = 'Bridge Officer', required=False, queryset=User.objects.all())
    bridgeAssistantOfficer1 = forms.ModelMultipleChoiceField(label = 'Bridge Assistant Officer', required=False, queryset=User.objects.all())
    bridgeAssistantOfficer2 = forms.ModelMultipleChoiceField(label = 'Bridge Assistant Officer', required=False, queryset=User.objects.all())
    bridgeAssistantOfficer3 = forms.ModelMultipleChoiceField(label = 'Bridge Assistant Officer', required=False, queryset=User.objects.all())

    #Computing Services Committee
    compservOfficer1 = forms.ModelMultipleChoiceField(label = 'Compserv Officer', queryset=User.objects.all())
    compservOfficer2 = forms.ModelMultipleChoiceField(label = 'Compserv Officer', required=False, queryset=User.objects.all())
    compservOfficer3 = forms.ModelMultipleChoiceField(label = 'Compserv Officer', required=False, queryset=User.objects.all())
    compservOfficer4 = forms.ModelMultipleChoiceField(label = 'Compserv Officer', required=False, queryset=User.objects.all())
    compservOfficer5 = forms.ModelMultipleChoiceField(label = 'Compserv Officer', required=False, queryset=User.objects.all())
    compservOfficer6 = forms.ModelMultipleChoiceField(label = 'Compserv Officer', required=False, queryset=User.objects.all())
    compservAssistantOfficer1 = forms.ModelMultipleChoiceField(label = 'Compserv Assistant Officer', required=False, queryset=User.objects.all())
    compservAssistantOfficer2 = forms.ModelMultipleChoiceField(label = 'Compserv Assistant Officer', required=False, queryset=User.objects.all())
    compservAssistantOfficer3 = forms.ModelMultipleChoiceField(label = 'Compserv Assistant Officer', required=False, queryset=User.objects.all())

    #Decal Committee
    decalOfficer1 = forms.ModelMultipleChoiceField(label = 'Decal Officer', queryset=User.objects.all())
    decalOfficer2 = forms.ModelMultipleChoiceField(label = 'Decal Officer', required=False, queryset=User.objects.all())
    decalOfficer3 = forms.ModelMultipleChoiceField(label = 'Decal Officer', required=False, queryset=User.objects.all())
    decalOfficer4 = forms.ModelMultipleChoiceField(label = 'Decal Officer', required=False, queryset=User.objects.all())
    decalOfficer5 = forms.ModelMultipleChoiceField(label = 'Decal Officer', required=False, queryset=User.objects.all())
    decalOfficer6 = forms.ModelMultipleChoiceField(label = 'Decal Officer', required=False, queryset=User.objects.all())
    decalAssistantOfficer1 = forms.ModelMultipleChoiceField(label = 'Decal Assistant Officer', required=False, queryset=User.objects.all())
    decalAssistantOfficer2 = forms.ModelMultipleChoiceField(label = 'Decal Assistant Officer', required=False, queryset=User.objects.all())
    decalAssistantOfficer3 = forms.ModelMultipleChoiceField(label = 'Decal Assistant Officer', required=False, queryset=User.objects.all())

    #Industrial Relations Committee
    indrelOfficer1 = forms.ModelMultipleChoiceField(label = 'Indrel Officer', queryset=User.objects.all())
    indrelOfficer2 = forms.ModelMultipleChoiceField(label = 'Indrel Officer', required=False, queryset=User.objects.all())
    indrelOfficer3 = forms.ModelMultipleChoiceField(label = 'Indrel Officer', required=False, queryset=User.objects.all())
    indrelOfficer4 = forms.ModelMultipleChoiceField(label = 'Indrel Officer', required=False, queryset=User.objects.all())
    indrelOfficer5 = forms.ModelMultipleChoiceField(label = 'Indrel Officer', required=False, queryset=User.objects.all())
    indrelOfficer6 = forms.ModelMultipleChoiceField(label = 'Indrel Officer', required=False, queryset=User.objects.all())
    indrelAssistantOfficer1 = forms.ModelMultipleChoiceField(label = 'Indrel Assistant Officer', required=False, queryset=User.objects.all())
    indrelAssistantOfficer2 = forms.ModelMultipleChoiceField(label = 'Indrel Assistant Officer', required=False, queryset=User.objects.all())
    indrelAssistantOfficer3 = forms.ModelMultipleChoiceField(label = 'Indrel Assistant Officer', required=False, queryset=User.objects.all())

    #Service Committee
    servOfficer1 = forms.ModelMultipleChoiceField(label = 'Service Officer', queryset=User.objects.all())
    servOfficer2 = forms.ModelMultipleChoiceField(label = 'Service Officer', required=False, queryset=User.objects.all())
    servOfficer3 = forms.ModelMultipleChoiceField(label = 'Service Officer', required=False, queryset=User.objects.all())
    servOfficer4 = forms.ModelMultipleChoiceField(label = 'Service Officer', required=False, queryset=User.objects.all())
    servOfficer5 = forms.ModelMultipleChoiceField(label = 'Service Officer', required=False, queryset=User.objects.all())
    servOfficer6 = forms.ModelMultipleChoiceField(label = 'Service Officer', required=False, queryset=User.objects.all())
    servAssistantOfficer1 = forms.ModelMultipleChoiceField(label = 'Service Assistant Officer', required=False, queryset=User.objects.all())
    servAssistantOfficer2 = forms.ModelMultipleChoiceField(label = 'Service Assistant Officer', required=False, queryset=User.objects.all())
    servAssistantOfficer3 = forms.ModelMultipleChoiceField(label = 'Service Assistant Officer', required=False, queryset=User.objects.all())

    #Student Relations Committee
    studrelOfficer1 = forms.ModelMultipleChoiceField(label = 'Studrel Officer', queryset=User.objects.all())
    studrelOfficer2 = forms.ModelMultipleChoiceField(label = 'Studrel Officer', required=False, queryset=User.objects.all())
    studrelOfficer3 = forms.ModelMultipleChoiceField(label = 'Studrel Officer', required=False, queryset=User.objects.all())
    studrelOfficer4 = forms.ModelMultipleChoiceField(label = 'Studrel Officer', required=False, queryset=User.objects.all())
    studrelOfficer5 = forms.ModelMultipleChoiceField(label = 'Studrel Officer', required=False, queryset=User.objects.all())
    studrelOfficer6 = forms.ModelMultipleChoiceField(label = 'Studrel Officer', required=False, queryset=User.objects.all())
    studrelAssistantOfficer1 = forms.ModelMultipleChoiceField(label = 'Studrel Assistant Officer', required=False, queryset=User.objects.all())
    studrelAssistantOfficer2 = forms.ModelMultipleChoiceField(label = 'Studrel Assistant Officer', required=False, queryset=User.objects.all())
    studrelAssistantOfficer3 = forms.ModelMultipleChoiceField(label = 'Studrel Assistant Officer', required=False, queryset=User.objects.all())

    #Tutoring Committee
    tutorOfficer1 = forms.ModelMultipleChoiceField(label = 'Tutoring Officer', queryset=User.objects.all())
    tutorOfficer2 = forms.ModelMultipleChoiceField(label = 'Tutoring Officer', required=False, queryset=User.objects.all())
    tutorOfficer3 = forms.ModelMultipleChoiceField(label = 'Tutoring Officer', required=False, queryset=User.objects.all())
    tutorOfficer4 = forms.ModelMultipleChoiceField(label = 'Tutoring Officer', required=False, queryset=User.objects.all())
    tutorOfficer5 = forms.ModelMultipleChoiceField(label = 'Tutoring Officer', required=False, queryset=User.objects.all())
    tutorOfficer6 = forms.ModelMultipleChoiceField(label = 'Tutoring Officer', required=False, queryset=User.objects.all())
    tutorAssistantOfficer1 = forms.ModelMultipleChoiceField(label = 'Tutoring Assistant Officer', required=False, queryset=User.objects.all())
    tutorAssistantOfficer2 = forms.ModelMultipleChoiceField(label = 'Tutoring Assistant Officer', required=False, queryset=User.objects.all())
    tutorAssistantOfficer3 = forms.ModelMultipleChoiceField(label = 'Tutoring Assistant Officer', required=False, queryset=User.objects.all())

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
