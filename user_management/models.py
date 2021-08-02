from django.db import models
from datetime import datetime
# Create your models here.


class Role(models.Model):
    role_name = models.CharField(max_length=50, null=True)
    create_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    create_by = models.IntegerField(blank=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    modify_by = models.IntegerField(blank=True)

    class Meta:
        db_table = "role"

    def __str__(self):
        return "%s" % self.role_name


class Organization(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    is_active = models.IntegerField(default=1)
    create_date = models.DateTimeField(default=datetime.now)
    create_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    modify_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "organization"

    def __str__(self):
        return "%s" % self.name


class User(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_active = models.IntegerField(default=1)
    # user_image = models.FileField(upload_to="uploads/", blank=True, null=True)
    role = models.ForeignKey(Role, default=1, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=datetime.now)
    create_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    modify_by = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "user"

    def __str__(self):
        return "%s" % self.name
