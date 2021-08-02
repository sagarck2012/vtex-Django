from user_management.models import *
from device_management.models import *

# Create your models here.


class ADCData(models.Model):
    device_reg = models.ForeignKey(DeviceReg, on_delete=models.CASCADE)
    adc_value = models.CharField(max_length=10)
    rssi_value = models.CharField(max_length=10)
    device_status = models.IntegerField(null=True)
    timestamp = models.DateTimeField(default=datetime.now)
    acq_script = models.CharField(max_length=100, default=None)
    topic = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = "adc_data"


class RPMData(models.Model):
    device_reg = models.ForeignKey(DeviceReg, on_delete=models.CASCADE)
    rpm_value = models.CharField(max_length=10)
    rpm_status = models.IntegerField(null=True)
    timestamp = models.DateTimeField(default=datetime.now)
    acq_script = models.CharField(max_length=100, default=None)
    topic = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = "rpm_data"
