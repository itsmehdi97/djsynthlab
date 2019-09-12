from django.conf import settings
from django.contrib.auth.forms import UserCreationForm 
from django import forms

from .models import User


class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    class Meta:
        model = User 
        fields = ['student_id', 'phone_number', 'email', 'last_name', 'password1', 'password2']

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        student_id = self.cleaned_data.get('student_id')
        email = self.cleaned_data.get('email')

        if (not student_id.isdigit()) or (not len(student_id) == 8):
            raise forms.ValidationError('invalid student id')

        if phone_number:
            if (not phone_number.isdigit()) or (not len(phone_number) == 11):
                print('inside')
                raise forms.ValidationError('invalid phone number')
            if User.objects.filter(phone_number=self.cleaned_data.get('phone_number')).exists():
                raise forms.ValidationError('phone number has to be unique')
            
        if email:
            if User.objects.filter(email=self.cleaned_data.get('email')).exists():
                raise forms.ValidationError('email address has to be unique')
        
        if User.objects.filter(student_id=self.cleaned_data.get('student_id')).exists():
            raise forms.ValidationError('student id has to be unique')
        

        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['student_id', 'phone_number', 'email', 'last_name', 'first_name',]