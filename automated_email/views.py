from django.views.generic.edit import FormView
from .forms import EmailsForm
from django import forms
from ga.models import Profile, Assessment

class EmailsView(FormView):
    template_name = 'automated_email/emails.html'
    form_class = EmailsForm
    success_url = "/admin"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context_all = Profile.objects.all()
        context_all = [str(t.id) for t in context_all]
        context['all'] = context_all
        
        context_unsubmited = []
        for t in [p.user for p in Profile.objects.all()]:
            for a in t.assessment_set.all():
                if (a.numOf4 is None or a.numOf3 is None or a.numOf2 is None or a.numOf1 is None):
                     context_unsubmited.append(str(t.profile.id))
                     break
        context['unsubmited'] = context_unsubmited
        
        context['assigned'] = [str(Profile.objects.get(user=t).id) 
            for t in Assessment.objects.values_list(
                'teacher', 
                flat=True
            ).distinct()
        ]
        
        return context
        
        
    def form_valid(self, form):
        
        object_line=form.cleaned_data['object_line']
        message = form.cleaned_data['message']

        emails = [(
            object_line, 
            message.replace(
                '{{username}}',r.user.username
            ),
            EMAIL_HOST_USER,
            (r.user.email,)
        ) for r in form.cleaned_data['recipients_list']]   
        
        send_mass_mail(emails, fail_silently=False)
        
        return super().form_valid(form)
        
        
