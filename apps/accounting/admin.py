from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
# from django_jalali.admin import ModelAdminJalaliMixin
from .models import *
from .forms import *


# admin.site.unregister(Group)


@admin.register(USER)
class USERAdmin(UserAdmin):
    form = USERChangeForm
    add_form = USERCreationForm
    
    list_display = ('last_name', 'first_name', 'national_code', 'mobile', 'role', 'insurance', 'insurance_expiration_date', 'is_staff', 'is_active',)
    ordering = ('role', 'insurance_expiration_date', 'last_name',)
    search_fields = ('last_name', 'mobile', 'national_code',)
    list_filter = ('role', 'is_active', 'is_staff',)
    filter_horizontal = ('user_permissions',)

    fieldsets = (
        ('مشخصات شخصی', {'fields': ('role','first_name', 'last_name', 'mobile','national_code', 'gender','insurance', 'insurance_expiration_date', 'income_percentage','password',)}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),)

    add_fieldsets = (
        (None, {'classes': ('wide',),'fields': ('role', 'first_name', 'last_name', 'mobile','national_code', 'gender','insurance', 'insurance_expiration_date', 'income_percentage', 'password1', 'password2'),}),)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly_fields.extend(['is_superuser', 'is_staff', 'groups', 'user_permissions'])
        return readonly_fields

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)


# FIELDSETS = ((None, {'fields': ('__all__',)}),(None, {'fields': ('is_active','created_at', 'updated_at', 'created_by', 'updated_by')}),)

class BaseAdminMixin:
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Hall)
class HallAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('name','is_active',)
    ordering = ('is_active', 'name',)
    readonly_fields = ('created_by', 'updated_by',)


@admin.register(Sport)
class SportAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('name','is_active',)
    ordering = ('is_active', 'name',)
    list_filter = ('is_active',)
    search_fields = ('name',)
    # raw_id_fields = ('some_foreign_key_field',)
    readonly_fields = ('created_by', 'updated_by',)


@admin.register(Course)
class CourseAdmin(BaseAdminMixin, admin.ModelAdmin):
    form = CourseForm
    
    list_display = ('sport','coach','days','start_time','price','capacity','is_active',)
    ordering = ('is_active', 'sport',)
    list_filter = ('hall','days','is_active',)
    search_fields = ('sport','coach',)
    readonly_fields = ('created_by', 'updated_by',)


@admin.register(AthleteCourse)
class AthleteCourseAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('athlete','course','enrollment_date','payment_status','payment_date',)
    ordering = ('is_active','enrollment_date',)
    list_filter = ('course','is_active',)
    search_fields = ('athlete','course',)
    readonly_fields = ('created_by', 'updated_by',)
    

@admin.register(Attendance)
class AttendanceAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('athlete_course','date','status',)
    ordering = ('date', 'status',)
    list_filter = ('status',)
    search_fields = ('athlete_course',)
    readonly_fields = ('created_by', 'updated_by',)


@admin.register(Cost)
class CostAdmin(BaseAdminMixin, admin.ModelAdmin):
    list_display = ('detail','cost',)
    ordering = ('cost',)
    search_fields = ('detail',)
    readonly_fields = ('created_by', 'updated_by', 'is_active',)