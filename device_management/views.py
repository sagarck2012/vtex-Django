from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from user_management.decorator import login_required
from .models import *
from .forms import DeviceRegForm
import paho.mqtt.client as mqtt
from threading import Timer
import time
import json
import random
import uuid


@login_required
def device_add(request):
    template = "device_management/device_registration.html"
    context = {'title': "Device Addition"}

    if request.method == 'GET':
        return render(request, template, context)

    if request.method == 'POST':
        device_id = request.POST['device_id']
        location = request.POST['location']
        installed_by = request.POST['installed_by']
        installation_date = request.POST['installation_date']
        machine_brand = request.POST['machine_brand']
        machine_no = request.POST['machine_no']

        device_exists = DeviceReg.objects.filter(device_id=device_id).count()

        context = {
            "device_id": device_id,
            "location": location,
            "installed_by": installed_by,
            "installation_date": installation_date,
            "machine_brand": machine_brand,
            "machine_no": machine_no
            }

        if device_exists > 0:
            messages.error(request, 'Device ID Already Exists!')
            return render(request, template, context)

        else:
            # print(f"device_id:{device_id}, location:{location}, installed_by:{installed_by}, installation_date"
            #       f":{installation_date}, machine_brand: {machine_brand}, machine_no:{machine_no}")
            # insert into db:
            DeviceReg.objects.create(
                device_id=device_id,
                location=location,
                installed_by=installed_by,
                installation_date=installation_date,
                knitting_machine_brand=machine_brand,
                knitting_machine_no=machine_no,
                reg_date=datetime.now(),
                reg_by=User(id=request.session['id']),
                organization=Organization.objects.get(pk=request.session['user_organization'])
            )
            messages.success(request, 'Device Added Successfully')
            return render(request, template, context)


@login_required
def device_list_inactive(request):
    template = "device_management/device_list_inactive.html"
    # template = "user_management/user_list2.html"
    context = {'title': "Inactive Device List"}
    if request.session['user_role'] == 'super admin':
        devices = DeviceReg.objects.filter(is_active=0).order_by('-pk')

    else:
        devices = DeviceReg.objects.filter(is_active=0, organization=
                                           request.session['user_organization']).order_by('-pk')
    # for item in devices:
    #     print(item.address)
    context['devices'] = devices
    # return HttpResponse('Inactive Device list')
    return render(request, template, context)


@login_required
def device_list_active(request):
    template = "device_management/device_list_active.html"
    # template = "user_management/user_list2.html"
    context = {'title': "Active Device List"}
    if request.session['user_role'] == 'super admin':
        devices = DeviceReg.objects.filter(is_active=1).order_by('-pk')
    else:
        devices = DeviceReg.objects.filter(is_active=1, organization=request.session['user_organization']).order_by('-pk')
    # for item in devices:
    #     print(item.address)
    context['devices'] = devices
    # return HttpResponse('Inactive Device list')
    return render(request, template, context)


@login_required
def device_edit(request, pk):
    # get user
    user = User.objects.get(pk=pk)
    role = Role.objects.all()
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
def device_activate(request, pk):
    DeviceReg.objects.filter(pk=pk).update(is_active=1)
    messages.success(request, "Device Active!")
    return redirect('device_management:device_list_inactive')


@login_required
def device_deactivate(request, pk):
    DeviceReg.objects.filter(pk=pk).update(is_active=0)
    messages.error(request, "Device Inactive!")
    return redirect('device_management:device_list_active')


@login_required
def device_reset(request, pk):
    device = DeviceReg.objects.get(pk=pk)
    id = uuid.uuid1()
    client_id = id.hex
    client = mqtt.Client(client_id)
    broker = "182.163.112.102"
    port = 1883
    # client.username_pw_set("ds_broker", "Ds@iot123")
    broker_user = "iotdatasoft"
    broker_password = "brokeriot2o2o"
    client.username_pw_set(username=broker_user, password=broker_password)
    client.connect(broker, port, 60)
    print("connecting to broker")
    reset_message = "{did: %s, reset: 1 }" % (device.device_id)
    client.publish("dsiot/vt/config", reset_message )  # publish
    messages.success(request, "Device Reset!")
    return redirect('device_management:device_list_active')


@login_required
def device_set_ap_mode(request, pk):
    device = DeviceReg.objects.get(pk=pk)
    id = uuid.uuid1()
    client_id = id.hex
    client = mqtt.Client(client_id)
    broker = "182.163.112.102"
    port = 1883
    # client.username_pw_set("ds_broker", "Ds@iot123")
    broker_user = "iotdatasoft"
    broker_password = "brokeriot2o2o"
    client.username_pw_set(username=broker_user, password=broker_password)
    client.connect(broker, port, 60)
    print("connecting to broker")
    reset_message = "{did: %s, reset: 1 }" % (device.device_id)
    client.publish("dsiot/vt/config", reset_message )  # publish
    messages.success(request, "Device Reset!")
    return redirect('device_management:device_list_active')


# def device_add(request):
#     if 'logged_in' in request.session:
#         if request.session['logged_in'] is True:
#             # session_module_list(request, request.session['user_role_id'])
#             form = DeviceRegForm()
#             template = "device_management/device_add.html"
#             context = {
#                 'title': "Device Registration",
#                 'form': form,
#             }
#             if request.method == 'POST':
#                 form = DeviceRegForm(request.POST)
#
#                 if form.is_valid():
#                     try:
#                         print("**************************************")
#                         form_instance = form.save()
#                         form_instance.save()
#                         messages.success(request, 'Data Created!')
#                         return redirect('wasa_utility:create_service_station')
#                     except Exception as e:
#                         error = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), e
#                         messages.error(request, error)
#                         return render(request, template, context)
#                 else:
#                     messages.error(request, "Invalid Form Request")
#                     return render(request, template, context)
#             else:
#                 return render(request, template, context)
#     else:
#         return redirect('wasa_utility:login')
