from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid

# Create your models here.

class User(AbstractUser):
    choices = (
        ('Специалист', 'Я регистрирую свои услуги как специалист'),
        ('Клиника', 'Я регистрирую услуги клиники как администратор')
    )
    type = models.TextField(choices=choices)
    username = None
    email = models.EmailField(unique=True, default=uuid.uuid4)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    clinic_name = models.CharField( max_length=255)

    last_name_or_clinic_name = models.CharField( max_length=255)

    # Имя для специалиста или адрес клиники
    first_name_or_clinic_address = models.CharField( max_length=255)

    # Отчество для специалиста или время работы клиники
    patronymic_or_clinic_hours = models.CharField( max_length=255, blank=True)

    # Пол для специалиста, пустое поле для клиники
    gender = models.CharField( max_length=10, blank=True)

    # Дата рождения для специалиста, пустое поле для клиники
    date_of_birth = models.DateField( null=True, blank=True)

    # Языки
    languages = models.JSONField( default=list, blank=True)

    other_language = models.CharField(blank=True, null=True, max_length=100)

    # WhatsApp
    whatsapp = models.CharField(blank=True, null=True, max_length=100)

    # Telegram
    telegram = models.CharField( max_length=20, blank=True)

    # Телефон
    phone = models.CharField(blank=True, null=True, max_length=100)

    # Страна
    country = models.CharField( max_length=100)

    # Город, населенный пункт
    city_or_locality = models.CharField( max_length=100)

    # Компьютерный анализ
    computer_analysis = models.TextField( blank=True)

    # Ученая степень для специалиста или вызов на дом для клиники
    academic_degree_or_home_call = models.TextField( blank=True)

    created_at = models.DateTimeField(auto_now=True)

    currency = models.CharField(max_length=100, null=True)

    def __str__(self) -> str:
        return f'{self.type} {self.email}'

class Service(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    persServ = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    emailS = models.EmailField()
    last_name_or_languages = models.CharField(max_length=100, blank=True, null=True)
    first_name_or_additional_language = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    service_type = models.JSONField( default=list)  # Сохраняем как строку с введенным текстом
    service_category = models.JSONField( default=list)  # Сохраняем как строку с введенным текстом
    age_from = models.CharField(max_length=100, blank=True, null=True)
    age_to = models.CharField(max_length=100, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    cost = models.IntegerField()
    online_payment = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    clinic_name_or_service_email = models.CharField(max_length=255, blank=True, null=True)
    service_address = models.CharField(max_length=255, blank=True, null=True)
    appointment_time = models.CharField(max_length=100, blank=True, null=True)
    home_service = models.TextField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    registration_time = models.DateTimeField(auto_now_add=True)

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    specialty = models.CharField(max_length=200, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now=True)

class GeneralInfo(models.Model):
    idObs = models.CharField(unique=True, max_length=128)
    gender = models.CharField(max_length=128)
    age = models.SmallIntegerField()
    weight = models.DecimalField(max_digits=8, decimal_places=2)
    height = models.DecimalField(max_digits=8, decimal_places=2)
    pregnancy = models.SmallIntegerField(default='')

class GeneralAnalyzes(models.Model):
    field_name = models.TextField(name='Название поля')
    tuple_element = models.TextField(name='Название в кортеже')

class ChemicalAnalyzes(models.Model):
    field_name = models.TextField(name='Название поля')
    tuple_element = models.TextField(name='Название в кортеже')

