from ga.models import Assessment, Indicator, Course, SemesterLU
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from ga.models import SEASON_CHOICES, Course
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime


class MyUserCreationForm(UserCreationForm):
 
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'
        self.fields['email'] = forms.EmailField(
            label="E-mail", 
            max_length=75
        )
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = super(MyUserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ['numOf4', 'numOf3', 'numOf2', 'numOf1']
        labels = {
            'numOf4': _('Exceeds Expectations - 4'),
            'numOf3': _('Meets Expectations - 3'),
            'numOf2': _('Needs Improvement - 2'),
            'numOf1': _('Unacceptable - 1'),
        }

    
class NewSemesterForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(NewSemesterForm, self).__init__(*args, **kwargs)
        
        cYear = datetime.datetime.now().year
        cTerm = SemesterLU.objects.latest().term
        iTerm = "A" if cTerm=="W" else "W"
        yearChoices = [(y,y) for y in range(cYear-5, cYear+3)]
        
        self.fields['year'] = forms.ChoiceField(
            choices=yearChoices, initial=cYear)
        self.fields['term'] = forms.ChoiceField(
            choices=SEASON_CHOICES, initial=iTerm)
        
        courses = Course.objects.all().filter(current_flag=True)
        teachers = User.objects.all()
        teachersID = [t.id for t in teachers]
        
        for course in courses:
            self.fields['{}'.format(course)] = forms.MultipleChoiceField(
                choices=zip(teachersID, teachers), required=False)
            self.fields['{}'.format(course)].label = '{}'.format(course)
        
    def clean(self):
        cleaned_data = super().clean()
        year = cleaned_data['year']
        term = cleaned_data['term']
        if SemesterLU.objects.filter(year=year, term=term).exists():
            raise forms.ValidationError(
                "This semester already exists."
            )
        
