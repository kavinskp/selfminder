import socket

from django.conf import settings
from django import forms
from django.core.mail import send_mail
from django.forms.widgets import RadioFieldRenderer
from django.http import HttpRequest
from django.utils.encoding import force_text
from django.utils.html import format_html_join
import re
import datetime
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from .models import Note, List, CustomUser,Owner


class NoteForm(forms.ModelForm):
    reminder_date = forms.DateField(widget=widgets.AdminDateWidget())

    class Meta:
        model = Note
        fields = ['title', 'reminder_date']


class ListForm(forms.ModelForm):

    class Meta:
        model = List
        fields = ['item', 'is_important']


class Login_Form(forms.Form):
    email = forms.CharField(max_length=256)
    password = forms.CharField(widget=forms.PasswordInput())
    def clean_email(self):
        cd=self.cleaned_data
        email=cd.get('email')
        if not re.match(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',email):
            raise forms.ValidationError("Please enter a valid email id")
        if not CustomUser.objects.filter(email=email):
            raise forms.ValidationError("This email id has not been registered yet")
        return email

   # def clean_password(self):
    #    cd=self.cleaned_data
     #  if len(password)<8:
      #      raise forms.ValidationError("Password should contain atleast 8 characters")
       # return password

    def clean(self):
        cd=self.cleaned_data
        email=cd.get('email')
        return cd

    def __init__(self, *args, **kwargs):
        super(Login_Form, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Emaid ID'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
#
#
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')
#
# class ProfileForm(forms.ModelForm):
#
#     class Meta:
#         model = Author
#         fields = ('email', 'phone')


class RadioFieldWithoutULRenderer(RadioFieldRenderer):
    def render(self):
        return format_html_join(
            '\n',
            '{0}',
            [(force_text(w),) for w in self],
        )

class RegisterOwner(forms.ModelForm):
    gender = forms.ChoiceField(
        widget=forms.RadioSelect(renderer=RadioFieldWithoutULRenderer),
        choices=Owner.GENDER_CHOICES
    )
    """
    entry_type = forms.ChoiceField(
        widget=forms.RadioSelect(renderer=RadioFieldWithoutULRenderer),
        choices=student.ENTRY_TYPE
    )
    """

    def clean_first_name(self):
        cd = self.cleaned_data
        first_name = cd.get('first_name')
        first_name=first_name.title()
        if not re.match(r'^([a-zA-Z]+)$', first_name):
            raise forms.ValidationError("Enter a valid name")
        return first_name

    def clean_middle_name(self):
        cd = self.cleaned_data
        middle_name = cd.get('middle_name')
        middle_name=middle_name.title()
        if not re.match(r'^([a-zA-Z]*)$', middle_name):
            raise forms.ValidationError("Enter a valid name")
        return middle_name

    def clean_last_name(self):
        cd = self.cleaned_data
        last_name = cd.get('last_name')
        last_name=last_name.title()
        if not re.match(r'^([a-zA-Z ]+)$', last_name):
            raise forms.ValidationError("Enter a valid name")
        return last_name

    def clean_date_of_joining(self):
        cd=self.cleaned_data
        date_of_joining=cd.get('date_of_joining')
        if not datetime.datetime.strptime(str(date_of_joining), '%Y-%m-%d'):
            raise forms.ValidationError("Enter the date in the given format (YYYY-MM-DD)")
        return date_of_joining

    def clean_dob(self):
        cd=self.cleaned_data
        dob=cd.get('dob')
        if not datetime.datetime.strptime(str(dob), '%Y-%m-%d'):
            raise forms.ValidationError("Enter the date in the given format (YYYY-MM-DD)")
        return dob

    #def clean_avatar(self):
    #    cd=self.cleaned_data
    #    avatar=cd.get('avatar')
    #   return avatar

    def clean_phone_number(self):
        cd=self.cleaned_data
        phone_number=cd.get('phone_number')
        if not re.match(r'^((\d+){10})$', phone_number):
            raise forms.ValidationError("Enter a valid mobile number")
        return phone_number


    def clean(self):
        cd=self.cleaned_data
        roll_no=cd.get('roll_no')
        first_name=cd.get('first_name')
        middle_name = cd.get('middle_name')
        last_name = cd.get('last_name')
        dob=cd.get('dob')
        avatar=cd.get('avatar')
        phone_number=cd.get('phone_number')
        return cd

    required_field = [
                      'first_name',
                      'last_name',
                      'gender',
                      'dob',
                      'phone_number',
                      'avatar'
                      ]

    class Meta:
        model = Owner
        fields = [
                  'first_name',
                  'middle_name',
                  'last_name',
                  'gender',
                  'dob',
                  'phone_number',
                  'avatar',
                  ]
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(RegisterOwner, self).__init__(*args, **kwargs)
        for field in RegisterOwner.required_field:
            self.fields[field].required = True


        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'First Name'
        })
        self.fields['middle_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Can be blank'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Surname or Initials'
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '10 digit mobile number'
        })
        self.fields['dob'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'YYYY-MM-DD',
        })

  #      self.fields['avatar'].widget.attrs.update({
   #         'class': 'form-control',
    #    })






class Signup_form(forms.ModelForm):
    email = forms.CharField(max_length=256)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Re-enter Password')

    def clean_email(self):
        cd = self.cleaned_data
        email = cd.get('email')
        if not re.match(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', email):
            raise forms.ValidationError("Please enter a valid email id")
        if CustomUser.objects.filter(email=email):
            raise forms.ValidationError("This email id has already been registered")
        return email

    def clean_password1(self):
        cd = self.cleaned_data
        password1 = cd.get('password1')
        if not re.match(r'(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&*-+=_/;:~.]).{6,}', password1):
            raise forms.ValidationError("Password should contain atleast 6 characters as well as a character,a digit and a special character")
        return password1

    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    required_field = ['email',
                      'password1',
                      'password2',
                      ]

    class Meta:
        model = CustomUser
        fields = ['email',
                  'password1',
                  'password2',
                  ]
        exclude = [
            'is_staff_account',
            'is_approved',
            'is_verified'
        ]

    def __init__(self, *args, **kwargs):
        super(Signup_form, self).__init__(*args, **kwargs)
        for field in Signup_form.required_field:
            self.fields[field].required = True


        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Your Email ID'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Retype Password'
        })


    def sendEmail(self, datas):

        link = settings.CURRENT_HOST_NAME +'activate/'+ datas['activation_key']
        subject = 'SelfMinder - Account Verification'
        message = 'Welcome to SelfMinder /n Click the following link to verify your account '+ link +' Stay with Us'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message,from_email, [datas['email']],fail_silently=False)




class LoginForm(forms.Form):
    email = forms.CharField(max_length=256)
    password = forms.CharField(widget=forms.PasswordInput())
    def clean_email(self):
        cd=self.cleaned_data
        email=cd.get('email')
        if not re.match(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',email):
            raise forms.ValidationError("Please enter a valid email id")
        if not CustomUser.objects.filter(email=email):
            raise forms.ValidationError("This email id has not been registered yet")
        return email

   # def clean_password(self):
    #    cd=self.cleaned_data
     #  if len(password)<8:
      #      raise forms.ValidationError("Password should contain atleast 8 characters")
       # return password

    def clean(self):
        cd=self.cleaned_data
        email=cd.get('email')
        return cd

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Emaid ID'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })


class passforgot(forms.Form):
    email=forms.CharField(max_length=256)

class passchange(forms.Form):
    email=forms.CharField(max_length=256)
    oldpass=forms.CharField(widget=forms.PasswordInput())
    newpass=forms.CharField(widget=forms.PasswordInput())
    newpass_again=forms.CharField(widget=forms.PasswordInput())
    def clean_email(self):
        cd=self.cleaned_data
        email=cd.get('email')
        if not re.match(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',email):
            raise forms.ValidationError("Please enter a valid email id")
        if CustomUser.objects.filter(email=email):
            raise forms.ValidationError("This email id has already been registered")
        return email

    def clean_newpass(self):
        cd=self.cleaned_data
        password1=cd.get('newpass')
        if len(password1)<8:
            raise forms.ValidationError("Password should contain atleast 8 characters")
        return password1

    def clean_newpass_again(self):
        cd=self.cleaned_data
        password1 = cd.get('newpass')
        password2 = cd.get('newpass_again')
        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    def clean(self):
        cd=self.cleaned_data
        email=cd.get('email')
        password1=cd.get('newpass')
        password2=cd.get('newpass_again')
        return cd

class confirmpass(forms.Form):
    passcode=forms.CharField(max_length=256)

class updateform(forms.ModelForm):
        class Meta:
            model = Owner
            fields = ['first_name','middle_name','last_name','gender','dob','phone_number']

