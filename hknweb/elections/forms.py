from django import forms
from .models import User
from .models import Group

class OfficerForm(forms.Form):

    users = User.objects.all()
    userChoices = [('', '-----------')] + [(x.username, (x.first_name + ' ' + x.last_name + ' ' + x.email)) for x in users]
    # Execs
    execPresident = forms.ChoiceField(label = 'President', choices = userChoices);
    execVicePresident = forms.ChoiceField(label = 'Vice President', choices = userChoices);
    execRecordingSecretary = forms.ChoiceField(label = 'Recording Secretary', choices = userChoices);
    execCorrespondingSecretary = forms.ChoiceField(label = 'Corresponding Secretary', choices = userChoices);
    execTreasurer = forms.ChoiceField(label = 'Treasurer', choices = userChoices);
    execDepartmentRelations = forms.ChoiceField(label = 'Department Relations', choices = userChoices);
    execAluminiRelations = forms.ChoiceField(label = 'Alumini Relations', choices = userChoices);

    #Activites Committee
    actOfficer1 = forms.ChoiceField(label = 'Activites Officer', choices = userChoices);
    actOfficer2 = forms.ChoiceField(label = 'Activites Officer', required=False, choices = userChoices);
    actOfficer3 = forms.ChoiceField(label = 'Activites Officer', required=False, choices = userChoices);
    actOfficer4 = forms.ChoiceField(label = 'Activites Officer', required=False, choices = userChoices);
    actOfficer5 = forms.ChoiceField(label = 'Activites Officer', required=False, choices = userChoices);
    actOfficer6 = forms.ChoiceField(label = 'Activites Officer', required=False, choices = userChoices);
    actAssistantOfficer1 = forms.ChoiceField(label = 'Activites Assistant Officer', required=False, choices = userChoices);
    actAssistantOfficer2 = forms.ChoiceField(label = 'Activites Assistant Officer', required=False, choices = userChoices);
    actAssistantOfficer3 = forms.ChoiceField(label = 'Activites Assistant Officer', required=False, choices = userChoices);

    #Bridge Committee
    bridgeOfficer1 = forms.ChoiceField(label = 'Bridge Officer', choices = userChoices);
    bridgeOfficer2 = forms.ChoiceField(label = 'Bridge Officer', required=False, choices = userChoices);
    bridgeOfficer3 = forms.ChoiceField(label = 'Bridge Officer', required=False, choices = userChoices);
    bridgeOfficer4 = forms.ChoiceField(label = 'Bridge Officer', required=False, choices = userChoices);
    bridgeOfficer5 = forms.ChoiceField(label = 'Bridge Officer', required=False, choices = userChoices);
    bridgeOfficer6 = forms.ChoiceField(label = 'Bridge Officer', required=False, choices = userChoices);
    bridgeAssistantOfficer1 = forms.ChoiceField(label = 'Bridge Assistant Officer', required=False, choices = userChoices);
    bridgeAssistantOfficer2 = forms.ChoiceField(label = 'Bridge Assistant Officer', required=False, choices = userChoices);
    bridgeAssistantOfficer3 = forms.ChoiceField(label = 'Bridge Assistant Officer', required=False, choices = userChoices);

    #Computing Services Committee
    compservOfficer1 = forms.ChoiceField(label = 'Compserv Officer', choices = userChoices);
    compservOfficer2 = forms.ChoiceField(label = 'Compserv Officer', required=False, choices = userChoices);
    compservOfficer3 = forms.ChoiceField(label = 'Compserv Officer', required=False, choices = userChoices);
    compservOfficer4 = forms.ChoiceField(label = 'Compserv Officer', required=False, choices = userChoices);
    compservOfficer5 = forms.ChoiceField(label = 'Compserv Officer', required=False, choices = userChoices);
    compservOfficer6 = forms.ChoiceField(label = 'Compserv Officer', required=False, choices = userChoices);
    compservAssistantOfficer1 = forms.ChoiceField(label = 'Compserv Assistant Officer', required=False, choices = userChoices);
    compservAssistantOfficer2 = forms.ChoiceField(label = 'Compserv Assistant Officer', required=False, choices = userChoices);
    compservAssistantOfficer3 = forms.ChoiceField(label = 'Compserv Assistant Officer', required=False, choices = userChoices);

    #Decal Committee
    decalOfficer1 = forms.ChoiceField(label = 'Decal Officer', choices = userChoices);
    decalOfficer2 = forms.ChoiceField(label = 'Decal Officer', required=False, choices = userChoices);
    decalOfficer3 = forms.ChoiceField(label = 'Decal Officer', required=False, choices = userChoices);
    decalOfficer4 = forms.ChoiceField(label = 'Decal Officer', required=False, choices = userChoices);
    decalOfficer5 = forms.ChoiceField(label = 'Decal Officer', required=False, choices = userChoices);
    decalOfficer6 = forms.ChoiceField(label = 'Decal Officer', required=False, choices = userChoices);
    decalAssistantOfficer1 = forms.ChoiceField(label = 'Decal Assistant Officer', required=False, choices = userChoices);
    decalAssistantOfficer2 = forms.ChoiceField(label = 'Decal Assistant Officer', required=False, choices = userChoices);
    decalAssistantOfficer3 = forms.ChoiceField(label = 'Decal Assistant Officer', required=False, choices = userChoices);

    #Industrial Relations Committee
    indrelOfficer1 = forms.ChoiceField(label = 'Indrel Officer', choices = userChoices);
    indrelOfficer2 = forms.ChoiceField(label = 'Indrel Officer', required=False, choices = userChoices);
    indrelOfficer3 = forms.ChoiceField(label = 'Indrel Officer', required=False, choices = userChoices);
    indrelOfficer4 = forms.ChoiceField(label = 'Indrel Officer', required=False, choices = userChoices);
    indrelOfficer5 = forms.ChoiceField(label = 'Indrel Officer', required=False, choices = userChoices);
    indrelOfficer6 = forms.ChoiceField(label = 'Indrel Officer', required=False, choices = userChoices);
    indrelAssistantOfficer1 = forms.ChoiceField(label = 'Indrel Assistant Officer', required=False, choices = userChoices);
    indrelAssistantOfficer2 = forms.ChoiceField(label = 'Indrel Assistant Officer', required=False, choices = userChoices);
    indrelAssistantOfficer3 = forms.ChoiceField(label = 'Indrel Assistant Officer', required=False, choices = userChoices);

    #Service Committee
    servOfficer1 = forms.ChoiceField(label = 'Service Officer', choices = userChoices);
    servOfficer2 = forms.ChoiceField(label = 'Service Officer', required=False, choices = userChoices);
    servOfficer3 = forms.ChoiceField(label = 'Service Officer', required=False, choices = userChoices);
    servOfficer4 = forms.ChoiceField(label = 'Service Officer', required=False, choices = userChoices);
    servOfficer5 = forms.ChoiceField(label = 'Service Officer', required=False, choices = userChoices);
    servOfficer6 = forms.ChoiceField(label = 'Service Officer', required=False, choices = userChoices);
    servAssistantOfficer1 = forms.ChoiceField(label = 'Service Assistant Officer', required=False, choices = userChoices);
    servAssistantOfficer2 = forms.ChoiceField(label = 'Service Assistant Officer', required=False, choices = userChoices);
    servAssistantOfficer3 = forms.ChoiceField(label = 'Service Assistant Officer', required=False, choices = userChoices);

    #Student Relations Committee
    studrelOfficer1 = forms.ChoiceField(label = 'Studrel Officer', choices = userChoices);
    studrelOfficer2 = forms.ChoiceField(label = 'Studrel Officer', required=False, choices = userChoices);
    studrelOfficer3 = forms.ChoiceField(label = 'Studrel Officer', required=False, choices = userChoices);
    studrelOfficer4 = forms.ChoiceField(label = 'Studrel Officer', required=False, choices = userChoices);
    studrelOfficer5 = forms.ChoiceField(label = 'Studrel Officer', required=False, choices = userChoices);
    studrelOfficer6 = forms.ChoiceField(label = 'Studrel Officer', required=False, choices = userChoices);
    studrelAssistantOfficer1 = forms.ChoiceField(label = 'Studrel Assistant Officer', required=False, choices = userChoices);
    studrelAssistantOfficer2 = forms.ChoiceField(label = 'Studrel Assistant Officer', required=False, choices = userChoices);
    studrelAssistantOfficer3 = forms.ChoiceField(label = 'Studrel Assistant Officer', required=False, choices = userChoices);

    #Tutoring Committee
    tutorOfficer1 = forms.ChoiceField(label = 'Tutoring Officer', choices = userChoices);
    tutorOfficer2 = forms.ChoiceField(label = 'Tutoring Officer', required=False, choices = userChoices);
    tutorOfficer3 = forms.ChoiceField(label = 'Tutoring Officer', required=False, choices = userChoices);
    tutorOfficer4 = forms.ChoiceField(label = 'Tutoring Officer', required=False, choices = userChoices);
    tutorOfficer5 = forms.ChoiceField(label = 'Tutoring Officer', required=False, choices = userChoices);
    tutorOfficer6 = forms.ChoiceField(label = 'Tutoring Officer', required=False, choices = userChoices);
    tutorAssistantOfficer1 = forms.ChoiceField(label = 'Tutoring Assistant Officer', required=False, choices = userChoices);
    tutorAssistantOfficer2 = forms.ChoiceField(label = 'Tutoring Assistant Officer', required=False, choices = userChoices);
    tutorAssistantOfficer3 = forms.ChoiceField(label = 'Tutoring Assistant Officer', required=False, choices = userChoices);

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

