from django import forms
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import USER, Course
import datetime


class USERCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="پسورد", widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="تایید پسورد", widget=forms.PasswordInput, required=False)

    class Meta:
        model = USER
        fields = ('role', 'first_name', 'last_name', 'mobile', 'gender')
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',}

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if role != 0:
            if not p1 or not p2:
                raise forms.ValidationError("برای این نوع کاربر پسورد الزامی است.")
            if p1 != p2:
                raise forms.ValidationError("پسوردها باهم مطابقت ندارند.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if self.cleaned_data.get('role') == 0:
            user.set_unusable_password()
        else:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class USERChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label="پسورد",
        help_text=("برای تغییر پسورد کلیک کنید"))

    class Meta:
        model = USER
        fields = '__all__'


class CustomTimeInput(forms.TimeInput):
    input_type = 'text'

    def format_value(self, value):
        if isinstance(value, datetime.time):
            return value.strftime('%H:%M')
        return value

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            # اگر ورودی فقط عدد باشد و تعداد ارقام مشخص نباشد
            if value.isdigit():
                if len(value) <= 2:
                    # مثلاً 18 -> 18:00
                    value = f"{value}:00"
                elif len(value) == 3:
                    # مثلاً 930 -> 09:30 (اضافه کردن صفر ابتدا)
                    value = f"0{value[0]}:{value[1:]}"
                elif len(value) == 4:
                    # مثلاً 1530 -> 15:30
                    value = f"{value[:2]}:{value[2:]}"
            try:
                parsed_time = datetime.datetime.strptime(value, '%H:%M').time()
                return parsed_time
            except ValueError:
                pass  # در صورت خطا ورودی رو همانطور که هست برمی‌گرداند
        return value


class CourseForm(forms.ModelForm):
    
    class Meta:
        model = Course
        # exclude = ('created_at', 'updated_at', 'created_by', 'updated_by',)
        fields = '__all__'
        widgets = {
            'start_time': CustomTimeInput(attrs={'placeholder': 'HH:MM'}),
            'end_time': CustomTimeInput(attrs={'placeholder': 'HH:MM'}),}

