import hashlib
from datetime import date

from datetime import timedelta
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from django.utils import timezone
from django.utils.crypto import random

from .forms import NoteForm, ListForm, Signup_form,Login_Form,LoginForm
from .models import Note, List, Owner, CustomUser
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import transaction
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin import widgets

import hashlib
import re
from pprint import pprint

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.crypto import random
from datetime import date, timedelta
from django.views.generic import UpdateView


# AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
# IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

@login_required
def userprofile(request, username):
    try:
        user = Owner.objects.get(username=username)
        idnumber = user.user_id
        custuser = Owner.objects.get(id=idnumber)
        obj = Owner.objects.get(user=request.user)
        if obj.username != username:
            return render(request, "401.html")
    except:
        return render(request, "404.html")
    return render(request, "reminder/profilepage.html", {'user': user, 'custuser': custuser})


@login_required()
def edit_profile(request):
    user=request.user
    user_instance = Owner.objects.get(user=user)







def create_note(request):
    if not request.user.is_authenticated():
        return render(request, 'reminder/login.html')
    else:
        form = NoteForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            #
         #   note.note_logo = request.FILES['note_logo']
         #  file_type = note.note_logo.url.split('.')[-1]
         #   file_type = file_type.lower()
         #    if file_type not in IMAGE_FILE_TYPES:
         #       context = {
         #           'note': note,
         #           'form': form,
         #           'error_message': 'Image file must be PNG, JPG, or JPEG',
         #       }
          #      return render(request, 'reminder/create_note.html', context)
            note.save()
            return render(request, 'reminder/detail.html', {'note': note})
        context = {
            'form': form,
        }
        return render(request, 'reminder/create_note.html', context)


def create_list(request, note_id):
    form = ListForm(request.POST or None, request.FILES or None)
    note = get_object_or_404(Note, pk=note_id)
    if form.is_valid():
        notes_lists = note.list_set.all()
        for s in notes_lists:
            if s.item == form.cleaned_data.get("item"):
                context = {
                    'note': note,
                    'form': form,
                    'error_message': 'You already added that list',
                }
                return render(request, 'reminder/create_list.html', context)
        list = form.save(commit=False)
        list.note = note
     #  list.audio_file = request.FILES['audio_file']
     #   file_type = list.audio_file.url.split('.')[-1]
     #   file_type = file_type.lower()
     #   if file_type not in AUDIO_FILE_TYPES:
     #       context = {
     #           'note': note,
     #           'form': form,
     #           'error_message': 'Audio file must be WAV, MP3, or OGG',
     #       }
     #      return render(request, 'reminder/create_list.html', context)

        list.save()
        return render(request, 'reminder/detail.html', {'note': note})
    context = {
        'note': note,
        'form': form,
    }
    return render(request, 'reminder/create_list.html', context)


def delete_note(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    notes = Note.objects.filter(user=request.user)
    return render(request, 'reminder/index.html', {'notes': notes})


def delete_list(request, note_id, list_id):
    note = get_object_or_404(Note, pk=note_id)
    list = List.objects.get(pk=list_id)
    list.delete()
    return render(request, 'reminder/detail.html', {'note': note})


def detail(request, note_id):
    if not request.user.is_authenticated():
        return render(request, 'registration/login_user.html')
    else:
        user = request.user
        note = get_object_or_404(Note, pk=note_id)
        return render(request, 'reminder/detail.html', {'note': note})


def important(request, list_id):
    list = get_object_or_404(List, pk=list_id)
   # try:
    if list.is_important:
            list.is_important = False
    else:
        list.is_important = True
    list.save()
    note=list.note
    #except (KeyError, List.DoesNotExist):
    return render(request,'reminder/detail.html',{'note':note})
   # return JsonResponse({'success': False})
   # else:
    #return JsonResponse({'success': True})

#
# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('profile_user')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user)
#     return render(request, 'reminder/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })

def important_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    if note.is_important:
            note.is_important = False
    else:
            note.is_important = True
    note.save()
    notes = Note.objects.filter(user=request.user)
    return render(request, 'reminder/index.html', {'notes': notes})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'registration/login_user.html')
    else:
        owner=Owner.objects.get(user=request.user)
        notes = Note.objects.filter(user=owner)
        list_results = List.objects.all()
        query = request.GET.get("q")
        if query:
            n = notes.filter(
                Q(title__icontains=query)
            ).distinct()
            l = list_results.filter(
                Q(item__icontains=query)
            ).distinct()
            if not n and not l:
                return render(request,'reminder/index.html',{'error': 'No Match found', 'query':'yes'})
            return render(request, 'reminder/index.html', {
                'notes': n,
                'lists': l,
                'query': 'yes',

            })
        else:
            return render(request, 'reminder/index.html', {'notes': notes})


def logout_user(request):
    logout(request)
    form = Login_Form(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'registration/login_user.html', context)




def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                cusowner=CustomUser.objects.get(user=request.user)
                notes = Note.objects.filter(user=cusowner.owner)
                return render(request, 'reminder/index.html', {'notes': notes})
            else:
                return render(request, 'reminder/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'reminder/login.html', {'error_message': 'Invalid login'})
    return render(request, 'reminder/login.html')


def register(request):
    form = Signup_form(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                notes = Note.objects.filter(user=request.user)
                return render(request, 'reminder/index.html', {'notes': notes})
    context = {
        'form': form,
    }
    return render(request, 'reminder/signup.html', context)


def signup(request):
    form1 = Signup_form()
    error = 'success'
    if request.method == 'POST':
        form1 = Signup_form(request.POST, request.FILES)
        if form1.is_valid():
            try:
                password1 = form1.cleaned_data['password1']
                password2 = form1.cleaned_data['password2']
                if password1 and password2 and password1 != password2:
                    raise forms.ValidationError("Passwords don't match")
                # temp = form1.save(commit=False)
                email = form1.cleaned_data['email']
                password = form1.cleaned_data['password2']
                random_number_string = str(random.random())
                random_number_string = random_number_string.encode('utf-8')
                salt = hashlib.sha1(random_number_string).hexdigest()[:5]
                salt = salt.encode('utf-8')
                usernamesalt = email
                usernamesalt = usernamesalt.encode('utf8')
                key = hashlib.sha1(salt + usernamesalt)
                key = key.hexdigest()
                activation_key = key
                key_expires = timezone.now() + timezone.timedelta(days=2)

                user = CustomUser.objects.create_user(email=email,
                                                      password=password,
                                                      activation_key=activation_key,
                                                      key_expires=key_expires
                                                      )

                datas = {}
                datas['email'] = email
                datas['activation_key'] = key

                form1.sendEmail(datas)

                msg = {
                    'page_title': 'SelfMinder | Signup success',
                    'title': 'Please Verify Email-ID',
                    'description': 'An email has been sent your mail ID.Please verify it to proceed',
                }
                return render(request, 'reminder/signup_success.html', {'message': msg})
            except forms.ValidationError:
                error = 'pwd_Owner'
    return render(request, "reminder/register.html", {'form1': form1})

def activation(request, key):
    activation_expired = False
    already_active = False
    try:
        user = CustomUser.objects.get(activation_key=key)
        user.is_active=True
    except CustomUser.DoesNotExist:
        msg = {
            'page_title': 'Expired Link',
            'title': 'Link Expired',
            'description': 'Please check whether you are clicking the latest sent to your mail'
        }
        return render(request, 'reminder/signup_success.html', {'message': msg})

    print(vars(user))
    # if user.is_verified == False:
    #     if timezone.now() > user.key_expires:
    #         activation_expired = True  # Display : offer to user to have another activation link (a link in template sending to the view new_activation_link)
    #         id_user = user.id
    #     else:  # Activation successful
    #       #  user.is_verified = True
    #         user.save()

    # If user is already active, simply display error message
   # else:
    already_active = True  # Display : error message
    return render(request, 'registration/activated_mail.html', locals())


def new_activation_link(request, user_id):
    form = Signup_form()
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        raise Http404
    if user is not None and not user.is_verified:
        random_number_string = str(random.random())
        random_number_string = random_number_string.encode('utf-8')
        salt = hashlib.sha1(random_number_string).hexdigest()[:5]
        salt = salt.encode('utf-8')
        usernamesalt = user.email
        usernamesalt = usernamesalt.encode('utf8')

        key = hashlib.sha1(salt + usernamesalt)
        key = key.hexdigest()
        user.activation_key = key
        user.key_expires = timezone.now() + timezone.timedelta(days=2)
        user.save()

        datas = {}
        datas['email'] = user.email
        datas['activation_key'] = key

        form.sendEmail(datas)
    msg = {
        'page_title': 'SelfMinder | Re-sent conformation mail',
        'title': 'Email re-sent',
        'description': 'An email has been sent your mail ID.Please verify it to proceed',
    }
    return render(request, 'reminder/signup_success.html', {'message': msg})




def lists(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'reminder/login.html')
    else:
        try:
            list_ids = []
            for note in Note.objects.filter(user=request.user):
                for list in note.list_set.all():
                    list_ids.append(list.pk)
            users_lists = List.objects.filter(pk__in=list_ids)
            if filter_by == 'important':
                users_lists = users_lists.filter(is_important=True)
        except Note.DoesNotExist:
            users_lists = []
        return render(request, 'reminder/lists.html', {
            'list_list': users_lists,
            'filter_by': filter_by,
        })



def userlogin(request):
    login_form = LoginForm()
    error = None
    if request.method == 'POST':
       # request.session.clear()
       # request.session['last_visit'] = None
      #  request.session['logged_first'] = True
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            try:
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                if not CustomUser.objects.get(email=email):
                    raise forms.ValidationError("Email ID is not registered!")

                user = authenticate(email=email, password=password)
                print('****')

                if user is not None:
                    obj = CustomUser.objects.get(email=email)
                    is_verified_user = getattr(obj, 'is_verified')
                   # is_filled_data = getattr(obj, 'has_filled_data')
                   # is_staff_acc = getattr(obj, 'is_staff_account')
                    print('is_verified_user=' + str(is_verified_user))
                    # app = CustomUser.objects.filter(email=user)
                    # print(app.values('is_approved') == False)
                    # if (not is_filled_data):
                    #     # return getdetails(request, is_staff_acc, user)
                    #     request.session['is_staff_acc'] = is_staff_acc
                    #     request.session['user_name'] = email
                    #     return redirect('getdetails')

                  #  elif is_verified_user:
                    if Owner.objects.filter(user=user):
                       # request.session['user_type'] = 'Owner'
                       # request.session['user_name'] = str(Owner.objects.get(user=user))
                        if user.is_active:
                            login(request, user)
                            cusowner = CustomUser.objects.get(user=request.user)
                            notes = Note.objects.filter(user=cusowner.owner)
                            return render(request, 'reminder/index.html', {'notes': notes})
                       #     for each in Owner.objects.filter(user=user):
                                # request.session['profile_pic'] = str(each.avatar)
                    #            request.session['roll_no'] = str(each.roll_no)
                    #            request.session['gender'] = str(each.gender)
                             #   request.session['profile_pic'] = str(each.avatar)
                        # print('user=' + str(request.session['gender']))
                        last_login = ''
                        #for obj in CustomUser.objects.filter(email=str(user)):
                        #    last_login = obj.last_login
                        # print('last_visit=' + str(last_login))
                        #if last_login:
                        #     request.session['last_visit'] = last_login.strftime("%d %B %Y at %l:%M:%S %p")
                        #     today = str(date.today())
                        #     # print('today='+str(today))
                        #     yesterday = str(date.today() - timedelta(1))
                        #     # print('yesterday='+str(yesterday))
                        #     last_login_date = str(last_login.strftime("%Y-%m-%d"))
                        #     # print('last_login_date='+str(last_login_date))
                        #     if last_login_date == today:
                        #         last_login_time = str(last_login.strftime(" at %l:%M:%S %p"))
                        #         request.session['last_visit'] = 'Today' + last_login_time
                        #     elif last_login_date == yesterday:
                        #         last_login_time = str(last_login.strftime(" at %l:%M:%S %p"))
                        #         request.session['last_visit'] = 'Yesterday' + last_login_time
                        # else:
                        #     request.session['last_visit'] = 'welcome'
                        # # print(request.session['last_visit'])
                        # login(request, user)
                        #
                        if request.POST.get('remember_me'):
                             request.session['remember_me'] = True
                        #     print('remember me set')
                        # else:
                        #     request.session.set_expiry(0)
                        #
                        # request.session['disp_batch'] = None
                        #return render(request,'reminder/index.html')
                    else:
                        # print('not approved')
                        request.session['delete_user'] = str(user)
                        request.session['email'] = email
                        msg = {
                            'page_title': 'SelfMinder | Not approved',
                            'title': 'Account not approved'
                        }
                        return render(request, 'prompt_pages/not_approved.html', {'message': msg})
                else:
                    # print('not valid')
                    msg = {
                        'page_title': 'SelfMinder | Login error',
                        'title': 'Invalid account',
                        'description': 'Email and password did not match!',
                    }
                    return render(request, 'prompt_pages/invalid_account.html', {'message': msg})
            except forms.ValidationError:
                error = 'emailerror'
                # else:
        # login_form = LoginForm()
        #error = 'emailerror'
    if request.session and 'remember_me' in request.session:
        cusowner = CustomUser.objects.get(user=request.user)
        notes = Note.objects.filter(user=cusowner.owner)
        return render(request,'reminder/index.html')
    return render(request, "registration/login_user.html", {'loginForm': login_form, 'error': error})

