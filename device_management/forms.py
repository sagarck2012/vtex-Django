from django import forms
from .models import DeviceReg

class DeviceRegForm(forms.Form):
    class Meta:
        model = DeviceReg
        exclude = ['is_active', 'reg_date', 'reg_by', 'modify_date', 'modify_by']