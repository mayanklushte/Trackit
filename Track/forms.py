from django import forms
from django.contrib.auth.models import User
from .models import register, comdetails, Event, message, relation
from django.forms import DateInput


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class Register_form(forms.ModelForm):

    class Meta:
        model = register
        exclude = ['user', 'address', 'state', 'pincode', 'Sex', 'profile_photo']


class c_details_form(forms.ModelForm):
    class Meta:
        model = comdetails
        fields = '__all__'
        exclude = ['status', 'company_Name']
        widgets = {
            'requirements': forms.Textarea(attrs={'cols': 80, 'rows': 10}),

        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
          'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
          'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats parses HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


class MessageForm(forms.ModelForm):
    class Meta:
        model = message
        fields = '__all__'
        exclude = ['sender', 'receiver', 'date', 'time']
        widgets = {
            'message': forms.Textarea(attrs={'cols': 100, 'rows': 10}),

        }
        labels = {
            "message": ""
        }


class RelationForm(forms.ModelForm):
    class Meta:
        model = relation
        exclude = ['sender_r', 'receiver_r']
