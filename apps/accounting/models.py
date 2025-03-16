from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator,MinValueValidator
# from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
from django.core.exceptions import ValidationError
import re
from django.contrib.humanize.templatetags.humanize import intcomma


class USERManager(BaseUserManager):
    def create_user(self, mobile, first_name, last_name, national_code, gender, role, insurance, insurance_expiration_date, income_percentage, password=None, **extra_fields):
        if not mobile:
            raise ValueError('موبایل را وارد کنید')

        user = self.model(
            mobile=mobile, 
            first_name=first_name, 
            last_name=last_name, 
            gender=gender, 
            role=role,
            national_code=national_code,
            insurance=insurance,
            insurance_expiration_date=insurance_expiration_date,
            income_percentage=income_percentage,
            **extra_fields)
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user
    
    def create_superuser(self, mobile, first_name, last_name, national_code, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(mobile, first_name, last_name, national_code, gender=True, role=2, insurance=False, insurance_expiration_date=None, income_percentage=0, password=password, **extra_fields)

    
class USER(AbstractUser,PermissionsMixin):
    mobile = models.CharField(max_length=11, unique=True,verbose_name='موبایل')
    activation_code = models.CharField(max_length=6, blank=True, null=True)
    GENDER = ((True, 'مرد'), (False, 'زن'))
    gender = models.BooleanField(choices=GENDER,verbose_name='جنسیت')
    ROLE_CHOICES = ((0, 'ورزشکار'),(1, 'مربی'),(2, 'اپراتور'),)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=0,verbose_name='نوع کاربر')
    national_code = models.CharField(max_length=10,unique=True,verbose_name='کد ملی')
    insurance = models.BooleanField(default=False, verbose_name='بیمه')
    insurance_expiration_date = models.DateField(blank=True,null=True,verbose_name='تاریخ انقضای بیمه')
    income_percentage = models.PositiveSmallIntegerField(default=0,verbose_name='درصد درآمد')

    username = None
    email = None

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'national_code',]

    objects = USERManager()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if self.role in [1, 2]:
            self.is_staff = True
        super().save(*args, **kwargs)
        
    def clean(self):
        """
        اعتبارسنجی داده‌های ورودی مدل.
        """
        super().clean()
        # اعتبارسنجی کد ملی: باید دقیقا 10 رقم باشد
        if not re.fullmatch(r'\d{10}', self.national_code):
            raise ValidationError({'national_code': "کد ملی باید دقیقا ۱۰ رقم باشد."})
        
        # اعتبارسنجی شماره موبایل: به عنوان مثال باید با '09' شروع شود و 11 رقم باشد
        if not re.fullmatch(r'09\d{9}', self.mobile):
            raise ValidationError({'mobile': "شماره موبایل باید با 09 شروع شده و 11 رقم باشد."})

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['date_joined']


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True,verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='زمان ایجاد شدن')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='زمان آخرین آپدیت')
    created_by = models.ForeignKey(USER, on_delete=models.DO_NOTHING, related_name='%(class)s_created',null=True, blank=True,verbose_name='ایجاد شده توسط')
    updated_by = models.ForeignKey(USER, on_delete=models.DO_NOTHING, related_name='%(class)s_updated',null=True, blank=True,verbose_name='آپدیت شده توسط')
    
    class Meta:
        abstract = True


class Hall(BaseModel):
    name = models.CharField(max_length=20,unique=True,verbose_name='نام سالن')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'سالن'
        verbose_name_plural = 'سالن‌ها'
        ordering = ['name']


class Sport(BaseModel):
    name = models.CharField(max_length=20,unique=True,verbose_name='رشته')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'رشته'
        verbose_name_plural = 'رشته‌ها'
        ordering = ['name']


class Course(BaseModel):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE,verbose_name = 'رشته')
    coach = models.ForeignKey(USER, on_delete=models.CASCADE,limit_choices_to={'role': 1},verbose_name='مربی')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE,verbose_name = 'سالن')
    DAYS = ((True, 'روزهای زوج'), (False, 'روزهای فرد'))
    days = models.BooleanField(choices=DAYS,verbose_name='روزهای کلاس')
    start_time = models.TimeField(verbose_name='زمان شروع کلاس')
    end_time = models.TimeField(verbose_name='زمان پایان کلاس')
    price = models.PositiveIntegerField(default=700000,validators=[MinValueValidator(100000),MaxValueValidator(99999999)],verbose_name='شهریه به تومان')
    capacity = models.PositiveSmallIntegerField(default=40,verbose_name='ظرفیت کلاس')
    
    def __str__(self):
        return f'{self.sport} - {self.coach}'
    
    @property
    def remaining_capacity(self):
        registered = self.athletecourse_set.count()
        return self.capacity - registered
    
    @property
    def formatted_tuition(self):
        return intcomma(self.tuition)
    
    class Meta:
        verbose_name = 'کلاس'
        verbose_name_plural = 'کلاس‌ها'
        ordering = ['sport']


class AthleteCourse(BaseModel):
    athlete = models.ForeignKey(USER, on_delete=models.CASCADE,limit_choices_to={'role': 0},verbose_name='ورزشکار')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name='کلاس')
    enrollment_date = models.DateField(auto_now_add=True,verbose_name='تاریخ ثبت‌نام')
    payment_status = models.BooleanField(default=False,verbose_name='پرداخت شده')
    payment_date = models.DateField(null=True, blank=True,verbose_name='تاریخ پرداخت')
    
    def __str__(self):
        return f'{self.athlete}'
    
    def fee_due_date(self):
        """
        تاریخ موعد پرداخت شهریه: اگر تاریخ پرداخت وجود داشته باشد، یک ماه بعد از آن،
        در غیر این صورت یک ماه بعد از تاریخ ثبت‌نام.
        """
        base_date = self.payment_date if self.payment_date else self.enrollment_date
        return base_date + relativedelta(months=1)
    
    @property
    def is_fee_overdue(self):
        """
        اگر تاریخ فعلی از تاریخ موعد پرداخت (fee_due_date) گذشته باشد و وضعیت پرداخت False باشد،
        آنگاه شهریه منقضی شده است.
        """
        due_date = self.fee_due_date()
        return timezone.now().date() > due_date and not self.payment_status
    
    class Meta:
        verbose_name = 'ثبت‌نام'
        verbose_name_plural = 'ثبت‌نام'
        ordering = ['payment_date']


class Attendance(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name='کلاس')
    athlete_course = models.ForeignKey(AthleteCourse, on_delete=models.CASCADE,verbose_name='ورزشکار')
    date = models.DateField(verbose_name='تاریخ')
    status = models.BooleanField(blank=True,verbose_name='حاضر')
    
    def __str__(self):
        return f'{self.athlete_course} در کلاس {self.course} در تاریخ {self.date} {self.status} بوده است'
    
    class Meta:
        verbose_name = 'حضور و غیاب'
        verbose_name_plural = 'حضور و غیاب'
        ordering = ['date']
      
        
class Cost(BaseModel):
    detail = models.TextField(max_length=1000,verbose_name='هزینه')
    cost = models.PositiveIntegerField(validators=[MinValueValidator(10000)],verbose_name='مبلغ به تومان')
    
    class Meta:
        verbose_name = 'هزینه'
        verbose_name_plural = 'هزینه‌ها'
        ordering = ['cost']