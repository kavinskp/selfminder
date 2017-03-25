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
from reminder.models import CustomUser, Owner
from reminder.forms import   LoginForm, passchange, Signup_form, RegisterOwner


def index(request):
    if request.session and 'remember_me' in request.session:
        return redirect('/')
    return render(request, "reminder/index.html")


@login_required
def userprofile(request, roll):
    try:
        user = Owner.objects.get(roll_no=roll)
        idnumber = user.user_id
        custuser = CustomUser.objects.get(id=idnumber)
        obj = Owner.objects.get(user=request.user)
        # rollnumber = user.roll_no
        # idnumber = user.user_id
        # custuser = CustomUser.objects.get(id=idnumber)
        if obj.roll_no != roll:
            return render(request, "401.html")
    except:
        return render(request, "404.html")
    return render(request, "registration/profilepage.html", {'user': user, 'custuser': custuser})


@login_required
def viewprofile(request):


    obj = Owner.objects.get(user=request.user)
    # staffobj=None
    idnumber = obj.user_id
    custuser = CustomUser.objects.get(id=idnumber)
    return render(request, "registration/viewprofile.html",
                  {'obj': obj, 'custuser': custuser})


# class UpdateProfile(UpdateView):
#     form_class = regstaff
#     template_name = 'edit_form.html'
#     success_url = '/update_status/'
#     slug = None
#
#     def user_passes_test(self, request):
#         if request.user.is_authenticated():
#             self.object = self.get_object()
#             return self.object.user == request.user
#         return False
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.user_passes_test(request):
#             return redirect_to_login(request.get_full_path())
#         return super(UpdateProfile, self).dispatch(
#             request, *args, **kwargs)
#
#     def get_object(self):
#         try:
#             obj = Owner.objects.get(user=self.request.user)
#             self.model = Owner
#             self.form_class = regstud
#         except Owner.DoesNotExist:
#             obj = staff.objects.get(user=self.request.user)
#             self.model = staff
#         return obj
#
#
# class UpdateProfilePreApproval(UpdateView):
#     form_class = regstaff
#     template_name = 'accounts/edit_profile_pre_approval.html'
#     success_url = '/details_submit_success'
#     slug = None
#
#     def user_passes_test(self, request):
#         if 'email' in request.session:
#             self.object = self.get_object()
#             return True
#         return False
#
#     def dispatch(self, request, *args, **kwargs):
#         if not self.user_passes_test(request):
#             return redirect_to_login(request.get_full_path())
#         return super(UpdateProfilePreApproval, self).dispatch(
#             request, *args, **kwargs)
#
#     def get_object(self):
#         requested_user = CustomUser.objects.get(email=self.request.session['email'])
#         try:
#             obj = Owner.objects.get(user=requested_user)
#             self.model = Owner
#             self.form_class = regstud
#         except Owner.DoesNotExist:
#             obj = staff.objects.get(user=requested_user)
#             self.model = staff
#         return obj
#
#
# def getdetails(request):
#     form_data = ''
#     acc = ''
#     error = False
#     if request.method == 'POST':
#         if 'staff' in request.POST:
#             form2 = RegisterOwner(request.POST, request.FILES)
#             if form2.is_valid():
#                 temp = form2.save(commit=False)
#                 designation = form2.cleaned_data.get("designation")
#                 avatar = form2.cleaned_data['avatar']
#                 random_number_string = str(random.random())
#                 random_number_string = random_number_string.encode('utf-8')
#                 salt = hashlib.sha1(random_number_string).hexdigest()[:5]
#                 salt = salt.encode('utf-8')
#                 usernamesalt = str(request.POST.get('user_name'))
#                 usernamesalt = usernamesalt.encode('utf8')
#
#                 key = hashlib.sha1(salt + usernamesalt)
#                 key = key.hexdigest()
#                 temp.activation_key = key
#                 temp.key_expires = timezone.now() + timezone.timedelta(days=2)
#
#                 user = CustomUser.objects.get(email=str(request.POST.get('user_name')))
#
#                 if designation == 'Principal':
#                     g = Group.objects.get(name='principal')
#                 elif designation == 'Professor':
#                     faculty_group_obj = Group.objects.get(name='faculty')
#                     faculty_group_obj.user_set.add(user)
#                     g = Group.objects.get(name='hod')
#                 elif designation == 'Network Admin':
#                     g = Group.objects.get(name='network_admin')
#                 elif designation == 'Hostel Admin':
#                     g = Group.objects.get(name='hostel_admin')
#                 else:
#                     g = Group.objects.get(name='faculty')
#                 g.user_set.add(user)
#                 temp.user = user
#                 temp.save()
#                 user.has_filled_data = True
#                 user.save()
#
#                 del request.session['user_name']
#
#                 msg = {
#                     'page_title': 'GCT | Details confirmation',
#                     'title': 'Details submitted',
#                     'description': 'You have to be approved by an authorized person in order to proceed',
#                     'trylogin': True
#                 }
#                 return render(request, 'prompt_pages/details_submit_success.html', {'message': msg})
#             else:
#                 form_data = form2
#                 acc = 'staff'
#
#         elif 'Owner' in request.POST:
#             form1 = RegisterOwner(request.POST, request.FILES)
#             if form1.is_valid():
#                 temp = form1.save(commit=False)
#                 try:
#                     batch_obj_posted = request.POST.get('batch')
#                     batch_obj = batch.objects.get(id=int(batch_obj_posted))
#                     got_department = request.POST.get('department')
#                     department_instance = department.objects.get(id=got_department)
#                     avatar = form1.cleaned_data['avatar']
#                     active_batch_obj = active_batches.objects.get(batch=batch_obj,
#                                                                   department=department_instance)
#                     sem = active_batch_obj.current_semester_number_of_this_batch
#                     # print(sem)
#                     temp.current_semester = sem
#                     temp.batch_id = int(batch_obj_posted)
#                     temp.qualification = str(request.POST.get('qualification'))
#                     temp.entry_type = str(request.POST.get('entrytype'))
#                     temp.department = department_instance
#
#                     random_number_string = str(random.random())
#                     random_number_string = random_number_string.encode('utf-8')
#                     salt = hashlib.sha1(random_number_string).hexdigest()[:5]
#                     salt = salt.encode('utf-8')
#                     usernamesalt = str(request.POST.get('user_name'))
#                     usernamesalt = usernamesalt.encode('utf8')
#
#                     key = hashlib.sha1(salt + usernamesalt)
#                     key = key.hexdigest()
#                     temp.activation_key = key
#                     temp.key_expires = timezone.now() + timezone.timedelta(days=2)
#
#                     user = CustomUser.objects.get(email=str(request.POST.get('user_name')))
#                     temp.user = user
#                     g = Group.objects.get(name='Owner')
#                     g.user_set.add(user)
#                     temp.save()
#                     user.has_filled_data = True
#                     user.save()
#                     # print(vars(temp))
#
#                     del request.session['user_name']
#                     del request.session['is_staff_acc']
#
#                     msg = {
#                         'page_title': 'GCT | Details confirmation',
#                         'title': 'Details submitted',
#                         'des'
#                         'cription': 'You have to be approved by an authorized person in order to proceed',
#                         'trylogin': True
#                     }
#                     return render(request, 'prompt_pages/details_submit_success.html', {'message': msg})
#                 except:
#                     form_data = form1
#                     acc = 'Owner'
#                     error = 'datamiss'
#
#             else:
#                 form_data = form1
#                 acc = 'Owner'
#
#     else:
#         try:
#             is_staff_acc = bool(request.session['is_staff_acc'])
#         except:
#             msg = {
#                 'page_title': 'GCT | Unauthorized Access',
#                 'title': 'Unauthorized Access',
#                 'description': 'You don\'t have privilege to access this resourse!',
#                 'login': True
#             }
#             return render(request, 'prompt_pages/error_page_base.html', {'message': msg})
#
#         if is_staff_acc:
#             form_data = RegisterStaff()
#             acc = 'staff'
#         else:
#             form_data = RegisterOwner()
#             acc = 'Owner'
#
#     try:
#         user_name = request.session['user_name']
#     except:
#         msg = {
#             'page_title': 'GCT | Resubmission',
#             'title': 'Details Already Submitted',
#             'description': 'You don\'t have privilege to access this resourse!',
#         }
#         return render(request, 'prompt_pages/error_page_base.html', {'message': msg})
#     # print(user_name)
#
#     department_list = department.objects.all()
#
#     return render(request, "fill_signup_details.html",
#                   {'form1': form_data, 'acc_type': acc, 'user': user_name, 'error': error, 'department_list': department_list})
#
#
# def get_current_batches_signup(request):
#     if request.method == 'POST':
#         if request.is_ajax():
#             dictionary = {}
#             chosen_programme = str(request.POST.get('qualification'))
#             chosen_entry_type = str(request.POST.get('entry_type'))
#             chosen_department = request.POST.get('department')
#             print(chosen_department)
#             department_instance = department.objects.get(id=chosen_department)
#
#             print('chosen_entry_type=' + str(chosen_entry_type))
#             print('chosen_programme_type=' + str(chosen_programme))
#
#             if chosen_programme == 'Phd':
#                 batch_objects = get_current_batches(department_instance,get_phd=True)
#             else:
#                 batch_objects = get_current_batches(department_instance)
#
#
#
#             list = []
#             for each in batch_objects:
#                 temp = {}
#                 temp['batch_obj'] = each['batch_obj']
#                 if chosen_entry_type != 'regular':
#                     batch_start_year = int(each['start_year'])
#                     batch_end_year = str(each['end_year'])
#                     batch_start_year_plus_one = str(batch_start_year + 1)
#                     temp['display_batch_text'] = batch_start_year_plus_one + '-' + batch_end_year
#                 else:
#                     temp['display_batch_text'] = str(each['start_year']) + '-' + str(each['end_year'])
#                 if each['programme'] == chosen_programme:
#                     list.append(temp)
#
#             pprint(list)
#
#             dictionary['list'] = list
#
#             return JsonResponse(dictionary)
#

def userlogin(request):
    login_form = LoginForm()
    error = None
    if request.method == 'POST':
        request.session.clear()
        request.session['last_visit'] = None
        request.session['logged_first'] = True
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            try:
                email = login_form.cleaned_data['email']
                password = login_form.cleaned_data['password']
                if not CustomUser.objects.get(email=email):
                    raise forms.ValidationError("Email ID is not registered!")

                user = authenticate(email=email, password=password)

                if user is not None:
                    obj = CustomUser.objects.get(email=email)
                    # print(vars(obj))
                    is_approved_user = getattr(obj, 'is_approved')
                    is_verified_user = getattr(obj, 'is_verified')
                    is_filled_data = getattr(obj, 'has_filled_data')
                    is_staff_acc = getattr(obj, 'is_staff_account')
                    print('is_verified_user=' + str(is_verified_user))
                    # app = CustomUser.objects.filter(email=user)
                    # print(app.values('is_approved') == False)
                    if is_verified_user:
                        if (not is_filled_data):
                            # return getdetails(request, is_staff_acc, user)
                            request.session['is_staff_acc'] = is_staff_acc
                            request.session['user_name'] = email
                            return redirect('getdetails')

                        elif is_approved_user:
                            if Owner.objects.filter(user=user):
                                request.session['user_type'] = 'Owner'
                                request.session['user_name'] = str(Owner.objects.get(user=user))
                                for each in Owner.objects.filter(user=user):
                                    # request.session['profile_pic'] = str(each.avatar)
                                    request.session['roll_no'] = str(each.roll_no)
                                    request.session['gender'] = str(each.gender)
                                    request.session['profile_pic'] = str(each.avatar)

                            # print('user=' + str(request.session['gender']))
                            last_login = ''
                            for obj in CustomUser.objects.filter(email=str(user)):
                                last_login = obj.last_login
                            # print('last_visit=' + str(last_login))
                            if last_login:
                                request.session['last_visit'] = last_login.strftime("%d %B %Y at %l:%M:%S %p")
                                today = str(date.today())
                                # print('today='+str(today))
                                yesterday = str(date.today() - timedelta(1))
                                # print('yesterday='+str(yesterday))
                                last_login_date = str(last_login.strftime("%Y-%m-%d"))
                                # print('last_login_date='+str(last_login_date))
                                if last_login_date == today:
                                    last_login_time = str(last_login.strftime(" at %l:%M:%S %p"))
                                    request.session['last_visit'] = 'Today' + last_login_time
                                elif last_login_date == yesterday:
                                    last_login_time = str(last_login.strftime(" at %l:%M:%S %p"))
                                    request.session['last_visit'] = 'Yesterday' + last_login_time
                            else:
                                request.session['last_visit'] = 'welcome'
                            # print(request.session['last_visit'])
                            login(request, user)

                            if request.POST.get('remember_me'):
                                request.session['remember_me'] = True
                                print('remember me set')
                            else:
                                request.session.set_expiry(0)

                            request.session['disp_batch'] = None
                            return redirect('/dashboard/')
                        else:
                            # print('not approved')
                            request.session['delete_user'] = str(user)
                            request.session['email'] = email
                            msg = {
                                'page_title': 'GCT | Not approved',
                                'title': 'Account not approved'
                            }
                            return render(request, 'prompt_pages/not_approved.html', {'message': msg})
                    else:
                        # print('not verified')
                        request.session['delete_user'] = str(user)
                        msg = {
                            'page_title': 'GCT | Verification error',
                            'title': 'Account not verified',
                            'description': 'Your email is not yet verified',
                        }
                        return render(request, 'prompt_pages/not_verified.html', {'message': msg, 'user': user})

                else:
                    # print('not valid')
                    msg = {
                        'page_title': 'GCT | Login error',
                        'title': 'Invalid account',
                        'description': 'Email and password did not match!',
                    }
                    return render(request, 'prompt_pages/invalid_account.html', {'message': msg})
            except forms.ValidationError:
                error = 'emailerror'
                # else:
        # login_form = LoginForm()
        error = 'emailerror'

    if request.session and 'remember_me' in request.session:
        return redirect('/dashboard/')
    return render(request, "accounts/login.html", {'loginForm': login_form, 'error': error})


@login_required
def changepass(request):
    change_pass = passchange()
    if request.method == 'POST':
        # emailid = request.POST['email']
        emailid = CustomUser.objects.get(email=request.user)
        oldpass = request.POST['oldpass']
        newpass1 = request.POST['newpass']
        newpass2 = request.POST['newpass_again']
        checker = authenticate(email=emailid, password=oldpass)
        if not re.match(r'(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&*-+=_/;:~]).{8,}', newpass1):
            msg = {
                'page_title': 'Update failure',
                'title': 'Profile not updated',
                'description': 'Password should contain atleast 8 characters as well as a character,a digit and a special character',
            }
            return render(request, "changepass.html", {'message': msg})
        elif newpass1 and newpass2 and newpass1 != newpass2:
            msg = {
                'page_title': 'Update failure',
                'title': 'Profile not updated',
                'description': 'Your new passwords does not match!Try again..',
            }
            return render(request, "changepass.html", {'message': msg})
        elif newpass1 == oldpass:
            msg = {
                'page_title': 'Update failure',
                'title': 'Profile not updated',
                'description': 'Your have used the same password! Use a different password..',
            }
            return render(request, "changepass.html", {'message': msg})
        elif checker is None:
            msg = {
                'page_title': 'Update failure',
                'title': 'Profile not updated',
                'description': 'Your have entered wrong old password!',
            }
            return render(request, "changepass.html", {'message': msg})
        elif checker is not None:
            u = CustomUser.objects.get(email=emailid)
            u.set_password(newpass1)
            u.save()
            msg = {
                'page_title': 'Update success',
                'title': 'Profile updated',
                'description': 'Your password has been successfully changed! '
                               'Please login in to continue to the site!',
            }
            return render(request, "prompt_pages/update_message.html", {'forgotpass': change_pass, 'message': msg})
        else:
            msg = {
                'page_title': 'Update failure',
                'title': 'Profile not updated',
                'description': 'Username and email id mismatch! Forgot your password? Try resetting it..',
            }
            return render(request, "changepass.html", {'message': msg})
    else:
        return render(request, "changepass.html", {'changepass': change_pass})


# @login_required
def userlogout(request):
    request.session.clear();
    logout(request)
    return HttpResponseRedirect('/')


def cancel(request):
    delete_user = str(request.session['delete_user'])
    CustomUser.objects.filter(email=delete_user).delete()
    msg = {
        'page_title': 'Deleted Success',
        'title': 'Account Deleted',
        'deleted_user': str(delete_user),
        'description': '\'s request canceled successfully...',
        'createnew': True
    }
    return render(request, 'prompt_pages/error_page_base.html', {'message': msg})


def homepagelogout(request):
    request.session.clear();
    logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    form1 = Signup_form()
    error = 'success'
    if request.method == 'POST':
        if request.POST.get('Owner_register'):
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

                    print('acc_type=' + str(request.POST.get('acc_type')))

                    acc_type = str(request.POST.get('acc_type'))

                    if (acc_type == 'staff'):
                        is_staff_acc = True
                    else:
                        is_staff_acc = False

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
                                                          is_staff_account=is_staff_acc,
                                                          activation_key=activation_key,
                                                          key_expires=key_expires
                                                          )

                    datas = {}
                    datas['email'] = email
                    datas['activation_key'] = key

                    form1.sendEmail(datas)

                    msg = {
                        'page_title': 'GCT | Signup success',
                        'title': 'Please Verify Email-ID',
                        'description': 'An email has been sent your mail ID.Please verify it to proceed',
                    }
                    return render(request, 'prompt_pages/signup_success.html', {'message': msg})
                except forms.ValidationError:
                    error = 'pwd_Owner'
    return render(request, "signup.html", {'form1': form1})


# View called from activation email. Activate user if link didn't expire (48h default), or offer to
# send a second link if the first expired.
def activation(request, key):
    activation_expired = False
    already_active = False
    try:
        user = CustomUser.objects.get(activation_key=key)
    except CustomUser.DoesNotExist:
        msg = {
            'page_title': 'Expired Link',
            'title': 'Link Expired',
            'description': 'Please check whether you are clicking the latest sent to your mail'
        }
        return render(request, 'prompt_pages/error_page_base.html', {'message': msg})

    print(vars(user))
    if user.is_verified == False:
        if timezone.now() > user.key_expires:
            activation_expired = True  # Display : offer to user to have another activation link (a link in template sending to the view new_activation_link)
            id_user = user.id
        else:  # Activation successful
            user.is_verified = True
            user.save()

    # If user is already active, simply display error message
    else:
        already_active = True  # Display : error message
    return render(request, 'prompt_pages/activated_mail.html', locals())


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
        'page_title': 'GCT | Re-sent conformation mail',
        'title': 'Email re-sent',
        'description': 'An email has been sent your mail ID.Please verify it to proceed',
    }
    return render(request, 'prompt_pages/signup_success.html', {'message': msg})


def details_submit_success(request):
    msg = {
        'page_title': 'GCT | Details confirmation',
        'title': 'Details submitted',
        'description': 'You have to be approved by an authorized person in order to proceed',
        'trylogin': True
    }
    return render(request, 'prompt_pages/details_submit_success.html', {'message': msg})


def updatestatus(request):
    for each in Owner.objects.filter(user=request.user):
        request.session['profile_pic'] = str(each.avatar)
        request.session['user_name'] = str(each)

    msg = {
        'page_title': 'Update success',
        'title': 'Profile updated',
        'description': 'Your profile has been successfully updated!'
    }
    return render(request, 'prompt_pages/update_message.html', {'message': msg})
