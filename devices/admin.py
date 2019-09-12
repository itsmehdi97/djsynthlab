from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.forms import ValidationError
from django.shortcuts import redirect
from django.contrib import messages

from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
from datetime import datetime

from .models import  Tool, Reservation, Attr, ToolAttr, ReservationAttr
from .forms import ReservationForm

from users.models import User

class AttrAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
admin.site.register(Attr, AttrAdmin)

class ToolAttrAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
admin.site.register(ToolAttr, ToolAttrAdmin)


# class StudentAdmin(admin.ModelAdmin):
#     fields = ['first_name', 'last_name']
#     search_fields = ['first_name', 'last_name']

# admin.site.register(Student, StudentAdmin)

class ToolAttrInline(admin.TabularInline):
    model = ToolAttr
    extra = 1


class ReservationAttrInline(admin.TabularInline):
    model = ReservationAttr
    extra = 1


class ToolAdmin(admin.ModelAdmin):
    inlines = [ToolAttrInline]
    list_display = ['name', 'desc']
    search_fields = ['name', 'desc']

admin.site.register(Tool, ToolAdmin)

class ReservationStatusListFilter(admin.SimpleListFilter):
    title = _('status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('in progress', _('in progress')),
            ('queued', _('queued')),
            ('expired', _('expired')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'in progress':
            return queryset.filter(start__lte=timezone.now(),
                                    end__gte=timezone.now())
        if self.value() == 'queued':
            return queryset.filter(start__gte=timezone.now(),
                                    end__gte=timezone.now())
        if self.value() == 'expired':
            return queryset.filter(end__lte=timezone.now())

class ReservationToolListFilter(admin.SimpleListFilter):
    title = _('tool')
    parameter_name = 'tool'

    def lookups(self, request, model_admin):
        tools = Tool.objects.all().values_list('name', flat=True).distinct()
        rv = []
        for tool in tools:
            rv.append((tool, _(tool)))
        return rv

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tool__name=self.value())
        else:
            return queryset


class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm
    fieldsets = [
        (None, {'fields': ['tool']}),
        ('DateTime Information', {'fields': ['start', 'end']}),
        ('User Information', {'fields': ['users', 'desc']}),
    ]
    search_fields = ['users__first_name', 'users__last_name', 'desc']
    inlines = [ReservationAttrInline]
    list_display = ['tool', 'start_datetime', 'end_datetime', 'status', 'reserved_by']
    list_per_page = 4
    ordering = ('start',)
    list_filter = (ReservationStatusListFilter,ReservationToolListFilter,)
    
    def save_model(self, request, obj, form, change):
        if (not request.user.is_superuser) and change:
            if request.user not in obj.users.all():
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Each record can only be modified by it's users.")
                return
        return super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if not request.user.is_superuser:
            if request.user not in obj.users.all():
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Each record can only be modified by it's users.")
                return
        return super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        print('INSIDE')
        if request.user.is_superuser:
            print('IM SUPER')
            super().delete_queryset(request, queryset)
        else:
            print('IM NOT SUPER')
            messages.set_level(request, messages.ERROR)
            messages.error(request, "This action has been restricted for you, since you are not a superuser.")  
            return
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        r = Reservation.objects.get(pk=object_id)
        if not request.user.is_superuser:
            if request.user not in r.users.all():
                extra_context = extra_context or {}
                extra_context['readonly'] = True
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)


    
admin.site.register(Reservation, ReservationAdmin)



