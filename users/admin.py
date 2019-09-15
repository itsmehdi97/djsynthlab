from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import RegisterForm
from .models import User

# class MyUserAdmin(admin.ModelAdmin):
#     list_display = ['student_id', 'email', 'first_name', 'last_name', 'is_superuser']


class MyUserAdmin(UserAdmin):
    list_display = ['last_name', 'first_name', 'student_id', 'email', 'is_superuser']
    fieldsets = ((None, {'fields': ('student_id', 'password')}), ('Personal info', {'fields': ('first_name',
    'last_name', 'email')}), ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), ('Important dates', {'fields': ('last_login', 'date_joined')}))

     
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('student_id', 'phone_number', 'email', 'last_name', 'first_name', 'password1', 'password2',)
        }),
    )
     

    
    def save_model(self, request, obj, form, change):
        
        if form.is_valid():
            print('is valid')
            return super().save_model(request, obj, form, change)
        else: return
    

admin.site.register(User, MyUserAdmin)

from djcelery.models import (
    TaskState, WorkerState, PeriodicTask, 
    IntervalSchedule, CrontabSchedule)

admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)