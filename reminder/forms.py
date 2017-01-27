from django import forms
from django.contrib.auth.models import User
from django.contrib.admin import widgets

from .models import Note, List


class NoteForm(forms.ModelForm):
   # reminder_date = forms.DateField(widget=widgets.AdminDateWidget)

    class Meta:
        model = Note
        fields = ['title', 'reminder_date']




class ListForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ['item', 'is_important']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
