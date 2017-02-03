from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from .forms import NoteForm, ListForm, UserForm #ProfileForm
from .models import Note, List #Author
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import transaction
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin import widgets

# AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
# IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


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
        return render(request, 'reminder/login.html')
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
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('profile_user')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
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
        return render(request, 'reminder/login.html')
    else:
        notes = Note.objects.filter(user=request.user)
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
    form = UserForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'reminder/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                notes = Note.objects.filter(user=request.user)
                return render(request, 'reminder/index.html', {'notes': notes})
            else:
                return render(request, 'reminder/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'reminder/login.html', {'error_message': 'Invalid login'})
    return render(request, 'reminder/login.html')


def register(request):
    form = UserForm(request.POST or None)
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
    return render(request, 'reminder/register.html', context)


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
