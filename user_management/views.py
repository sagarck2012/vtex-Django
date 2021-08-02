from django.shortcuts import render, redirect, Http404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
import hashlib
from user_management.decorator import *
import sys
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from viyellatex.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
# Create your views here.


def login(request):
    if 'logged_in' in request.session:
        if request.session['logged_in'] is True:
            return redirect("viyellatex:home")
    else:
        return render(request, 'user_management/login.html')


def login_validate(request):
    if request.method == 'POST':
        password = request.POST['pass']
        password_enc = hashlib.sha1(password.encode('utf-8')).hexdigest()
        username = request.POST['username']
        print(f"username: {username} & Password: {password_enc}")
        try:
            user = User.objects.get(name=username)

        except Exception as e:
            print(e)
            user = None

        if user is None:
            messages.error(request, 'Username not found!')
            return render(request, 'user_management/login.html', dict(username=username, password=password))
        else:
            if user.password == password_enc and user.name == username:
                if user.is_active == 1:
                    try:
                        request.session['logged_in'] = True
                        request.session['user_name'] = user.name
                        request.session['user_email'] = user.email
                        request.session['id'] = user.pk
                        request.session['user_role_id'] = user.role_id
                        request.session['user_role'] = user.role.role_name
                        request.session['user_organization'] = user.organization.id
                        request.session['organization_name'] = user.organization.name

                    except Exception as e:
                        print(e)
                        pass

                    return redirect("viyellatex:home")
                else:
                    messages.error(request, 'Your Account is not active. Please contact Admin.')
                    return render(request, 'user_management/login.html', dict(username=username, password=password))
            else:
                messages.error(request, 'Incorrect Password!')
                username = username
                password = password
                return render(request, 'user_management/login.html', dict(username=username, password=password))
    else:
        raise Http404("Page does not exist!")


def logout(request):
    if 'logged_in' in request.session:
        del request.session['logged_in']
    if 'user_name' in request.session:
        del request.session['user_name']
    if 'user_role' in request.session:
        del request.session['user_role']
    if 'user_role_id' in request.session:
        del request.session['user_role_id']
    if 'id' in request.session:
        del request.session['id']
    if 'user_organization' in request.session:
        del request.session['user_organization']
    if 'organization_name' in request.session:
        del request.session['organization_name']
    return redirect('user_management:login')


@login_required
def user_registration(request):
    organization = Organization.objects.filter(is_active=1)
    context = {
        "organization": organization
    }
    if request.method == 'GET':
        return render(request, 'user_management/user_registration2.html', context)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        password = request.POST['pass']
        repeat_password = request.POST['repeat_password']
        password_enc = hashlib.sha1(password.encode('utf-8')).hexdigest()

        context = {
            "username": username,
            "email": email,
            "address": address,
            "phone": phone,
            "organization": organization
        }

        # check if username already exists
        user_exists = User.objects.filter(name=username).count()

        # check if email already exists
        email_exists = User.objects.filter(email=email).count()

        # check if phone already exists
        phone_exists = User.objects.filter(phone=phone).count()

        if user_exists > 0:
            messages.error(request, 'Username Already Exists!')

            return render(request, 'user_management/user_registration2.html', context)
        elif email_exists > 0:
            messages.error(request, 'Email Already Exists!')
            return render(request, 'user_management/user_registration2.html', context)
        elif phone_exists > 0:
            messages.error(request, 'Phone No. Already Exists!')
            return render(request, 'user_management/user_registration2.html', context)
        elif password != repeat_password:
            messages.error(request, 'Password & Repeat Password does not match!')
            return render(request, 'user_management/user_registration2.html', context)
        else:
            print(f"Name:{username}, email:{email}, address: {address}, phone: {phone}, password: {password}")
            # insert into db:
            # if not super admin then organization is logged in users' organization
            if request.session['user_role'] != 'super admin':
                print("User not super admin")
                User.objects.create(
                    name=username,
                    address=address,
                    email=email,
                    phone=phone,
                    password=password_enc,
                    organization=Organization.objects.get(pk=request.session['user_organization']),
                    role=Role.objects.get(role_name='view only'),
                    create_date=datetime.now(),
                    create_by=request.session['id']

                )
                # else organization is chosen organization
            else:
                print("User is super admin")
                User.objects.create(
                    name=username,
                    address=address,
                    email=email,
                    phone=phone,
                    password=password_enc,
                    organization=Organization.objects.get(pk=request.POST['organization']),
                    role=Role.objects.get(role_name='view only'),
                    create_date=datetime.now(),
                    create_by=request.session['id']

                )
            messages.success(request, 'User Registered Successfully')
            # return render(request, 'user_management/user_registration2.html')
            return redirect('user_management:user_list')


@login_required
def user_list(request):
    if request.session['user_role'] == 'super admin':
        users = User.objects.filter(is_active=1).order_by('-id')
    else:
        users = User.objects.filter(is_active=1, organization= request.session['user_organization']).order_by('-id')
    context = {
        "users": users
    }
    return render(request, 'user_management/user_list2.html', context)


@login_required
def user_edit(request, pk):
    # get user
    user = User.objects.get(pk=pk)
    role = Role.objects.exclude(role_name='super admin')
    if request.method == 'GET':
        context = {
            "id": user.id,
            "username": user.name,
            "email": user.email,
            "address": user.address,
            "phone": user.phone,
            "user_role": user.role.role_name,
            "role": role

        }

        print(f"context is---------- {context}")
        return render(request, 'user_management/user_edit2.html', context)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        user_role = request.POST['role']
        role = Role.objects.all()
        context = {
            "id": user.id,
            "username": username,
            "email": email,
            "address": address,
            "phone": phone,
            "user_role": user_role,
            "role": role
        }

        # check if username already exists
        user_exists = User.objects.filter(name=username).exclude(pk=pk).count()

        # check if email already exists
        email_exists = User.objects.filter(email=email).exclude(pk=pk).count()

        # check if phone already exists
        phone_exists = User.objects.filter(phone=phone).exclude(pk=pk).count()

        if user_exists > 0:
            messages.error(request, 'Username Already Exists!')

            return render(request, 'user_management/user_edit2.html', context)
        elif email_exists > 0:
            messages.error(request, 'Email Already Exists!')
            return render(request, 'user_management/user_edit2.html', context)
        elif phone_exists > 0:
            messages.error(request, 'Phone No. Already Exists!')
            return render(request, 'user_management/user_edit2.html', context)
        else:
            print(f"Name:{username}, email:{email}, address: {address}, phone: {phone}")
            # Update info:
            User.objects.filter(pk=user.id).update(
                name=username,
                address=address,
                email=email,
                phone=phone,
                role=Role.objects.get(pk=user_role),
                modify_date=datetime.now(),
                modify_by=request.session['id']

            )
            messages.success(request, 'User Updated Successfully')
            # return render(request, 'user_management/user_edit2.html', context)
            return redirect('user_management:user_list')


@login_required
def user_delete(request, pk):
    User.objects.filter(pk=pk).update(is_active=0)
    messages.error(request, "User Removed!")
    return redirect('user_management:user_list')


# def reset_password(request):
#     if request.method == 'GET':
#         return render(request, 'user_management/reset_password_of_particular_user.html')
#     if request.method == 'POST':
#         username_or_email = request.POST['username_or_email']
#         password = request.POST['pass']
#         retype_password = request.POST['retype_pass']
#
#         context = {
#             "username_or_email": username_or_email
#         }
#         # check if username or exists
#         user_exists = User.objects.filter(name=username_or_email)
#         email_exists = User.objects.filter(email=username_or_email)
#
#         if len(user_exists) != 0:
#             user_id = user_exists[0].id
#         if len(email_exists) != 0:
#             user_id = email_exists[0].id
#
#         if len(user_exists) == 0 and len(email_exists) == 0:
#             messages.error(request, "Username or Email does not exist!")
#             return render(request, 'user_management/reset_password_of_particular_user.html', context)
#         else:
#             if password == retype_password:
#                 password = hashlib.sha1(password.encode('utf-8')).hexdigest()
#                 User.objects.filter(pk=user_id).update(password=password)
#                 messages.success(request, "Password Reset Successful")
#                 return redirect('user_management:login')
#             else:
#                 messages.error(request, "Password & Confirm Password does not match")
#                 return render(request, 'user_management/reset_password_of_particular_user.html', context)


def password_reset_mail(send_to, user_id):
    subject = 'Reset Your password'
    context = {
        "user_id": user_id
    }
    html_message = render_to_string('user_management/password_reset_mail.html', context)
    plain_message = strip_tags(html_message)
    email_from = EMAIL_HOST_USER
    recipient_list = [send_to]
    try:
        send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
    except Exception as e:
        error = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), e
        print(f"Error:{error}")


def reset_password(request):
    if request.method == 'GET':
        return render(request, 'user_management/reset_password2.html')
    if request.method == 'POST':
        email_reset = request.POST['email_reset']

        context = {
            "email_reset": email_reset
        }
        # check if username or exists

        email_exists = User.objects.filter(email=email_reset)

        if len(email_exists) != 0:
            user_id = email_exists[0].id
            password_reset_mail(email_reset, user_id)
            messages.success(request, "Password reset link sent to your email")
            return render(request, 'user_management/login.html')

        else:
            messages.error(request, "Email does not exist!")
            return render(request, 'user_management/reset_password2.html', context)


def reset_password_of_particular_user(request, pk):
    context = {
        'id': pk
    }
    if request.method == 'GET':
        return render(request, 'user_management/reset_password_of_particular_user.html', context)
    if request.method == 'POST':
        password = request.POST['new_password']
        retype_password = request.POST['retype_password']
        if password == retype_password:
            password = hashlib.sha1(password.encode('utf-8')).hexdigest()
            User.objects.filter(pk=context["id"]).update(password=password)
            messages.success(request, "Password Reset Successful")
            return redirect('user_management:login')
        else:
            messages.error(request, "Password & Confirm Password does not match")
            return render(request, 'user_management/reset_password_of_particular_user.html', context)


@login_required
def change_password(request):
    if request.method == 'GET':
        return render(request, 'user_management/change_password2.html')
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        retype_password = request.POST['retype_password']

        context = {
            "current_password": current_password,
            "new_password": new_password,
            "retype_password": retype_password
        }
        # check if current password is correct
        password_from_db = User.objects.get(id=request.session['id']).password
        if password_from_db == hashlib.sha1(current_password.encode('utf8')).hexdigest():
            if new_password == retype_password:
                User.objects.filter(pk=request.session['id']).update(
                    password=hashlib.sha1(new_password.encode('utf8')).hexdigest()
                )
                messages.success(request, "Password Updated Successfully")
                # return render(request, 'user_management/change_password2.html')
                return redirect('user_management:logout')
            else:
                messages.error(request, "New Password and Confirm New Password does not match!")
                return render(request, 'user_management/change_password2.html', context)

        else:
            messages.error(request, "Incorrect Current Password!")
            return render(request, 'user_management/change_password2.html', context)


@login_required
def user_profile(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            "id": user.id,
            "username": user.name,
            "email": user.email,
            "address": user.address,
            "phone": user.phone,

        }

        print(f"context is---------- {context}")
        return render(request, 'user_management/user_profile.html', context)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        context = {
            "id": user.id,
            "username": username,
            "email": email,
            "address": address,
            "phone": phone
        }

        # check if username already exists
        user_exists = User.objects.filter(name=username).exclude(pk=pk).count()

        # check if email already exists
        email_exists = User.objects.filter(email=email).exclude(pk=pk).count()

        # check if phone already exists
        phone_exists = User.objects.filter(phone=phone).exclude(pk=pk).count()

        if user_exists > 0:
            messages.error(request, 'Username Already Exists!')

            return render(request, 'user_management/user_profile.html', context)
        elif email_exists > 0:
            messages.error(request, 'Email Already Exists!')
            return render(request, 'user_management/user_profile.html', context)
        elif phone_exists > 0:
            messages.error(request, 'Phone No. Already Exists!')
            return render(request, 'user_management/user_profile.html', context)
        else:
            print(f"Name:{username}, email:{email}, address: {address}, phone: {phone}")
            # Update info:
            User.objects.filter(pk=user.id).update(
                name=username,
                address=address,
                email=email,
                phone=phone,

                modify_date=datetime.now(),
                modify_by=request.session['id']

            )
            messages.success(request, 'Profile Updated Successfully')
            # return render(request, 'user_management/user_edit2.html', context)
            return redirect('user_management:user_profile', user.id)


@login_required
def organization_reg(request):

    if request.method == 'GET':
        return render(request, 'user_management/organization_reg.html')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']

        context = {
            "name": name,
            "email": email,
            "address": address,
            "phone": phone
        }

        org_exists = Organization.objects.filter(phone=phone, is_active=1).count()
        if org_exists > 0:
            messages.error(request, 'Organization Already Registered!')
            return render(request, 'user_management/organization_reg.html', context)
        else:
            Organization.objects.create(
                name=name,
                address=address,
                email=email,
                phone=phone,
                create_date=datetime.now(),
                create_by=request.session['id']
            )
            messages.success(request, 'Organization Registered Successfully')
            return redirect('user_management:organization_list')


@login_required
def organization_list(request):
    organizations = Organization.objects.filter(is_active=1).order_by('-id')
    context = {
        "organizations": organizations
    }
    return render(request, 'user_management/organizations_list.html', context)


@login_required
def organization_edit(request, pk):
    organization = Organization.objects.get(pk=pk)
    if request.method == 'GET':
        context = {
            "id": organization.id,
            "name": organization.name,
            "email": organization.email,
            "address": organization.address,
            "phone": organization.phone,

        }
        return render(request, 'user_management/organization_edit.html', context)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']

        context = {
            "id": organization.id,
            "name": name,
            "email": email,
            "address": address,
            "phone": phone
        }

        org_exists = Organization.objects.exclude(id=pk).filter(phone=phone, is_active=1).count()
        if org_exists > 0:
            messages.error(request, 'Phone No. Already Registered!')
            return render(request, 'user_management/organization_edit.html', context)
        else:
            Organization.objects.filter(pk=pk).update(
                name=name,
                address=address,
                email=email,
                phone=phone,
                modify_date=datetime.now(),
                modify_by=request.session['id']
            )
            messages.success(request, 'Organization Info Updated Successfully')
            return redirect('user_management:organization_list')


@login_required
def organization_delete(request, pk):
    Organization.objects.filter(pk=pk).update(is_active=0)
    messages.error(request, "Organization Removed!")
    return redirect('user_management:organization_list')





