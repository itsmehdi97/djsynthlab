from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Reservation

from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime


class ReservationForm(forms.ModelForm):
    start = forms.DateTimeField(required=True)
    end = forms.DateTimeField(required=True)
    email_reminder = forms.BooleanField(required=False, 
                                        help_text=_('Mark this if you want to get an email one day before your reservation time begins.'))
    class Meta:
        model = Reservation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        # self.fields['start'] = JalaliDateField(label=_('start'), # date format is  "yyyy-mm-dd"
        #     widget=AdminJalaliDateWidget # optional, to use default datepicker
        # )

        # you can added a "class" to this field for use your datepicker!
        # self.fields['date'].widget.attrs.update({'class': 'jalali_date-date'})

        self.fields['start'] = SplitJalaliDateTimeField(label=_('start'), 
            widget=AdminSplitJalaliDateTime # required, for decompress DatetimeField to JalaliDateField and JalaliTimeField
        )

        self.fields['end'] = SplitJalaliDateTimeField(label=_('end'), 
            widget=AdminSplitJalaliDateTime # required, for decompress DatetimeField to JalaliDateField and JalaliTimeField
        )

    #TODO: auth user should be selected as users field.
    def clean(self):
        start = self.cleaned_data.get('start')
        
        if not start:
            raise forms.ValidationError('')
        end = self.cleaned_data.get('end')
        if not end:
            raise forms.ValidationError('')
        now = timezone.now()
        if start < now or end < now:
            raise forms.ValidationError("Reservation date-time can't be in the past!")

        if end <= start:
            raise forms.ValidationError("'start' date-time must be less than or equal 'end' date-time!")
        
        qs1 = Reservation.objects.filter(tool__name=self.cleaned_data.get('tool'),
                                        start__lte=start,
                                        end__gte=start)
        qs2 = Reservation.objects.filter(tool__name=self.cleaned_data.get('tool'),
                                        start__lte=end,
                                        end__gte=end) 
        qs3 = Reservation.objects.filter(tool__name=self.cleaned_data.get('tool'),
                                        start__gte=start,
                                        end__lte=end)
        if self.instance:
            qs1 = qs1.exclude(pk=self.instance.pk)
            qs2 = qs2.exclude(pk=self.instance.pk)
            qs3 = qs3.exclude(pk=self.instance.pk)
        if qs1.exists() or qs2.exists() or qs3.exists():
            raise forms.ValidationError("Your reservation time conflicts with another record!")
        
        return self.cleaned_data
