from user_management.models import *
# Create your models here.


class DeviceReg(models.Model):
    device_id = models.CharField(max_length=50)
    # lat = models.FloatField()
    # lng = models.FloatField()
    rpm_status = models.IntegerField(default=0)
    location = models.CharField(max_length=100)
    installed_by = models.CharField(max_length=50, null=True, blank=False)
    installation_date = models.DateTimeField(default=datetime.now)
    # organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    knitting_machine_brand = models.CharField(max_length=20, null=True, blank=False)
    knitting_machine_no = models.CharField(max_length=8, null=True, blank=False)
    is_active = models.IntegerField(default=0)
    reg_date = models.DateTimeField(default=datetime.now)
    reg_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True)
    modify_by = models.IntegerField(null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table = "device_reg"


class DeviceLog(models.Model):
    device_reg = models.ForeignKey(DeviceReg, on_delete=models.CASCADE)
    # firmware_update = models.IntegerField(default=0)
    # firmware_version = models.CharField(max_length=5, null=True)
    normal_reset = models.IntegerField(default=0)
    reset_to_ap_mode = models.IntegerField(default=0)
    set_data_interval = models.IntegerField(default=0)
    set_delay = models.IntegerField(default=0)
    # ip = models.CharField(max_length=20, null=True)
    # mac = models.CharField(max_length=20, null=True)
    # memory_status = models.CharField(max_length=20, null=True)
    # run_time = models.CharField(max_length=20, null=True)
    # status = models.IntegerField(null=True)
    timestamp = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "device_reply_log"


class ConfigLog(models.Model):
    device_reg = models.ForeignKey(DeviceReg, on_delete=models.CASCADE)
    normal_reset = models.IntegerField(default=0)
    reset_to_ap_mode = models.IntegerField(default=0)
    set_data_interval = models.CharField(max_length=5)
    set_delay = models.CharField(max_length=5)
    configured_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "device_config_log"


class MQTTTopics(models.Model):
    server_pub_topic = models.CharField(max_length=50, default=None)
    server_sub_topic = models.CharField(max_length=50, default=None)
    msg = models.TextField(blank=True)

    class Meta:
        db_table = "MQTT_topics"

    def __str__(self):
        return "%s" % self.msg


class DeviceThreshold(models.Model):
    threshold_type = models.CharField(max_length=50)
    threshold_value = models.IntegerField()
    create_date = models.DateTimeField(default=datetime.now)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    modify_date = models.DateTimeField(null=True)
    modify_by = models.IntegerField(null=True)

    class Meta:
        db_table = "device_threshold"

    def __str__(self):
        return "%s" % self.threshold_type


