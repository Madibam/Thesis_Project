from django.contrib import admin
from django.db import models
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django import forms
from automated_email.views import EmailsView
from .views import NewSemesterView
from .forms import MyUserCreationForm
from .models import (Program, Course, Attribute, 
                     Indicator, AssessmentMethod, Assessment,
                     SemesterLU)


class MyAdminSite(AdminSite):
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('new_semester/', self.admin_view(NewSemesterView.as_view())),
            path('emails/', self.admin_view(EmailsView.as_view())),
        ]
        return my_urls + urls

    
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username','password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        })
    )
    

MyUserAdmin.add_form = MyUserCreationForm
MyUserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'email', 'password1', 'password2',)
    }),
)
admin.site.unregister(User)


class CourseAdmin(admin.ModelAdmin):
    filter_horizontal = ('teachers',)
    exclude = ('current_flag',)

                
class AssessmentMethodInline(admin.StackedInline):
    model = AssessmentMethod
    exclude = ('current_flag',)
    filter_horizontal = ('programs',)
    can_delete = True
    extra = 1


class IndicatorAdmin(admin.ModelAdmin):
    filter_horizontal = ('introduced', 'taught', 'used')
    exclude = ('current_flag',)
    inlines = (AssessmentMethodInline,)

    
class AttributeAdmin(admin.ModelAdmin):
    exclude = ('current_flag',)
    ordering = ('name',)
 
    
class ProgramAdmin(admin.ModelAdmin):
    exclude = ('current_flag',)
    
    def get_queryset(self, request):
        qs = super(ProgramAdmin, self).get_queryset(request)
        return qs.filter(current_flag=True)
    
    
class AssessmentAdmin(admin.ModelAdmin):
    fields = ('teacher', 'program', 'numOf4', 'numOf3', 'numOf2', 'numOf1')
    readonly_fields=('program', 'teacher')
    
    list_display=('pk', 'indicator', 'course', 'program', 'teacher', 'numOf4', 'numOf3', 'numOf2', 'numOf1')
    
    def course(self, obj):
        return obj.assessmentMethod.course
    course.admin_order_field = 'assessmentMethod__course'
       
    def indicator(self, obj):
        return obj.assessmentMethod.indicator
    indicator.admin_order_field = 'assessmentMethod__indicator'
    
    def get_actions(self, request):
        actions = super(AssessmentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False
        
    def get_queryset(self, request):
        qs = super(AssessmentAdmin, self).get_queryset(request)
        return qs.filter(semester=SemesterLU.objects.latest())
 
 
admin_site = MyAdminSite(name='myadmin') 
admin_site.register(User, MyUserAdmin)
admin_site.register(Program, ProgramAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Attribute, AttributeAdmin)
admin_site.register(Indicator, IndicatorAdmin)
admin_site.register(Assessment, AssessmentAdmin)


