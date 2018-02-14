from ga.models import Assessment, Indicator, Course, SemesterLU
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from ga.models import SEASON_CHOICES, Course, Profile
import datetime

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
        
class IndicatorCourseAdminForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ['course']
     
    course = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Introduced in',
            is_stacked=False
        )
    )
    
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
        
        courses = Course.objects.all()
        teachers = Profile.objects.all()
        teachersID = [t.user.id for t in teachers]
        
        for course in courses:
            self.fields['{}'.format(course)] = forms.MultipleChoiceField(
                choices=zip(teachersID, teachers), required=False)
            self.fields['{}'.format(course)].label = '{}'.format(course)
        
    
