from django.shortcuts import render, redirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import *
from device_management.models import *
# from user_management.models import *
# from django.contrib import messages
from user_management.decorator import *
from datetime import datetime, timedelta
import pytz
import simplejson
from django.db import connection
from . import raw_sql_query
# from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

today = datetime.now(pytz.timezone("Asia/Dhaka"))


def get_device_status(device_id):
    try:
        last_rpm_data = RPMData.objects.filter(device_reg=device_id).latest('timestamp')
        rpm_value = int(last_rpm_data.rpm_value)
        today_tz_removed = today.replace(tzinfo=None)  # removing timezone info from today
        print(f"today_tz_removed{today_tz_removed}")
        try:
            threshold_set_at_db = DeviceThreshold.objects.get(threshold_type='device_inactive').threshold_value
        except ObjectDoesNotExist:
            threshold_set_at_db = 30
        print(f"threshold_set_at_db: {threshold_set_at_db} minutes")
        threshold = today_tz_removed - timedelta(minutes=threshold_set_at_db)
        print(f"So threshold time is : {threshold}")
        print(f"Current time is  {today_tz_removed}")
        print(f"last_rpm data @ : {last_rpm_data.timestamp}")
        try:
            if last_rpm_data.timestamp < threshold:
                device_status = 0
            else:
                device_status = 1
        except:
            device_status = 0
    except ObjectDoesNotExist:
        device_status = 0
        rpm_value = 0

    print(f"So device_status: {device_status}")
    return device_status, rpm_value


def machine_data(request):
    if request.session['user_role'] == 'super admin':
        all_active_device = DeviceReg.objects.filter(is_active=1).order_by('device_id')
        offline = DeviceReg.objects.filter(rpm_status=0, is_active=1).count()
    else:
        all_active_device = DeviceReg.objects.filter(is_active=1, organization=request.session['user_organization'])\
                            .order_by('device_id')
        offline = DeviceReg.objects.filter(rpm_status=0, is_active=1,
                                           organization=request.session['user_organization']).count()
    total = len(all_active_device)

    online = total - offline

    # print(f"timestamp: {today}")
    '''
    Calculating Runtime of machine for current date:
    rmp < 10: rpm_status = 0
    10<rpm<20: rpm_status = 2
    rpm > 20: rpm_status = 1
    rpm data is received per minute from device.
    In super ideal case we should receive (24*60) = 1440 rpm_status in a day and if all of them are
    rpm_status = 1 we shall consider 100% runtime
    [1440 times rpm_status=1 on current date is equivalent to 100%]
    So for a particular moment of a day for [x times rpm_status = 1] then runtime = (100/1440)*x = 0.069*x%
    '''

    res = {}
    machine_list = []
    for data in all_active_device:
        device_status, rpm_value = get_device_status(data.id)
        res['id'] = data.id
        res['machine_no'] = data.knitting_machine_no
        res['rpm_status'] = data.rpm_status
        res['device_status'] = device_status
        res['rpm_value'] = rpm_value
        rpm_status_1_today = RPMData.objects.filter(rpm_status=1, device_reg=data.id,
                                                    timestamp__date=today.date()).count()
        print(f"RMP status 1 today:{rpm_status_1_today}")
        res['runtime'] = round(rpm_status_1_today * 0.069)
        print(f"Runtime:{res['runtime']}")
        if res['runtime'] > 100:
            res['runtime'] = 100
        # res['runtime'] = 50.50
        machine_list.append(res.copy())
    context = {
        'today': today.strftime('%d %B, %Y %I:%M %p'),
        'total': total,
        'online': online,
        'offline': offline,
        'machine_list': machine_list

    }

    return context


@login_required
def home(request):
    context = machine_data(request)
    return render(request, "viyellatex/home5.html", context)


def get_machine_data(request):
    context = machine_data(request)
    return HttpResponse(simplejson.dumps(context), content_type='application/json')


def get_all(cursor):
    """
    Return all rows from a cursor as a dict
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def detail(request, pk):
    device_data = DeviceReg.objects.get(id=pk)
    rpm = RPMData.objects.filter(device_reg=pk, timestamp__date=today.date()).last()
    rpm_status_1_today = RPMData.objects.filter(rpm_status=1, device_reg=pk,
                                                timestamp__date=today.date()).count()
    if rpm is None:
        rpm_value = 0
    else:
        rpm_value = rpm.rpm_value
    context = {
        'device_data': device_data,
        'rpm_value': rpm_value,
        'rpm_status_1_today': rpm_status_1_today,
    }
    return render(request, "viyellatex/detail.html", context)


def chart_data(duration, device_reg_id):
    x_axis_data = []
    area_graph_y_axis_data = []
    bar_graph_y_axis_data = []
    line_graph_y_axis_data = []
    if duration == '1':
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        query = raw_sql_query.get_avg_rssi_values_per_hour(device_reg_id)
        query2 = raw_sql_query.get_avg_rpm_values_and_count_per_hour(device_reg_id)
        # print(f"Query is {query}")
        cursor.execute(query)
        cursor2.execute(query2)
        query_data = get_all(cursor)
        query_data2 = get_all(cursor2)
        # print(query_data)
        # print(query_data2)

        for i in range(0, 24):
            if i < 10:
                x_axis_data.append("0"+str(i)+":00")
            else:
                x_axis_data.append(str(i)+":00")

        # get y_axis_data for area_graph
        for x in range(0, 24):
            if len(query_data) > 0:
                for data in query_data:
                    # print(type(data['HOUR']))
                    if data['HOUR'] == x:
                        y = data['RSSI']
                        # print(f"Matched hour {data['HOUR']} & Data: {data['RSSI']}")
                        break
                    else:
                        y = 0
            else:
                y = 0
            area_graph_y_axis_data.append(float(y))

        # get y_axis_data for bar_graph & line_graph
        for x in range(0, 24):
            if len(query_data2) > 0:
                for data in query_data2:
                    # print(type(data['HOUR']))
                    if data['HOUR'] == x:
                        y1 = data['RPM']
                        y2 = data['COUNT']
                        # print(f"Matched hour {data['HOUR']} & Data: {data['RPM']}, {data['COUNT']}")
                        break
                    else:
                        y1 = 0
                        y2 = 0
            else:
                y1 = 0
                y2 = 0
            line_graph_y_axis_data.append(float(y1))
            bar_graph_y_axis_data.append(float(y2))
    else:
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        query = raw_sql_query.get_avg_rssi_values_per_day(duration, device_reg_id)
        query2 = raw_sql_query.get_avg_rpm_values_and_count_per_day(duration, device_reg_id)
        # print(f"Query is {query}")
        # print(f"Query2 is {query2}")
        cursor.execute(query)
        cursor2.execute(query2)
        query_data = get_all(cursor)
        query_data2 = get_all(cursor2)
        # print(query_data)
        x_axis_data = []
        for i in range(int(duration), 0, -1):
            day = today.date()-timedelta(days=i)
            x_axis_data.append(day)
        # get y_axis_data for area_graph
        for x in x_axis_data:
            if len(query_data) > 0:
                for data in query_data:
                    # print(data['DAY'])
                    # print(x)
                    if data['DAY'] == x:
                        # print("matched")
                        y = data['RSSI']
                        break
                    else:
                        y = 0
            else:
                y = 0
            area_graph_y_axis_data.append(float(y))

        # get y_axis_data for bar graph and line graph

        for x in x_axis_data:
            if len(query_data2) > 0:
                for data in query_data2:
                    # print(data['DAY'])
                    # print(x)
                    if data['DAY'] == x:
                        # print("matched")
                        y1 = data['RPM']
                        y2 = data['COUNT']
                        # print(f"Matched day {data['DAY']} & Data: {data['RPM']}, {data['COUNT']}")
                        break
                    else:
                        y1 = 0
                        y2 = 0
            else:
                y1 = 0
                y2 = 0
            line_graph_y_axis_data.append(float(y1))
            bar_graph_y_axis_data.append(float(y2))

        # Convert x-axis date to str for jsonify

        for x in x_axis_data:
            x_str = x.strftime('%d %B,%Y')
            x_axis_data[x_axis_data.index(x)] = x_str

    # print(f"Y-axis data: {area_graph_y_axis_data}")
    # print(f"Y1-axis data: {line_graph_y_axis_data}")
    # print(f"Y2-axis data: {bar_graph_y_axis_data}")
    # print(f"X-axis data: {x_axis_data}")

    result = {
        'x_axis_data': x_axis_data,
        'area_graph_y_axis': area_graph_y_axis_data,
        'line_graph_y_axis': line_graph_y_axis_data,
        'bar_graph_y_axis': bar_graph_y_axis_data
    }

    return result


def get_chart_data(request, pk):
    day = request.GET['day']
    device_reg_id = pk
    result = chart_data(day, device_reg_id)
    return HttpResponse(simplejson.dumps(result), content_type='application/json')



