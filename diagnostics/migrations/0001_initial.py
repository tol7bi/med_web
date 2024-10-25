# Generated by Django 3.2.13 on 2024-07-15 10:00

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('type', models.TextField(choices=[('Специалист', 'Я регистрирую свои услуги как специалист'), ('Клиника', 'Я регистрирую услуги клиники как администратор')])),
                ('email', models.EmailField(default=uuid.uuid4, max_length=254, unique=True)),
                ('clinic_name', models.CharField(max_length=255)),
                ('last_name_or_clinic_name', models.CharField(max_length=255)),
                ('first_name_or_clinic_address', models.CharField(max_length=255)),
                ('patronymic_or_clinic_hours', models.CharField(blank=True, max_length=255)),
                ('gender', models.CharField(blank=True, max_length=10)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('languages', models.JSONField(blank=True, default=list)),
                ('other_language', models.CharField(blank=True, max_length=100, null=True)),
                ('whatsapp', models.CharField(blank=True, max_length=100, null=True)),
                ('telegram', models.CharField(blank=True, max_length=20)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(max_length=100)),
                ('city_or_locality', models.CharField(max_length=100)),
                ('computer_analysis', models.TextField(blank=True)),
                ('academic_degree_or_home_call', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('currency', models.CharField(max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ChemicalAnalyzes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Название поля', models.TextField()),
                ('Название в кортеже', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GeneralAnalyzes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Название поля', models.TextField()),
                ('Название в кортеже', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GeneralInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idObs', models.CharField(max_length=128, unique=True)),
                ('gender', models.CharField(max_length=128)),
                ('age', models.SmallIntegerField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=8)),
                ('height', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pregnancy', models.SmallIntegerField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('last_name_or_languages', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name_or_additional_language', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=10, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('service_type', models.JSONField(default=list)),
                ('service_category', models.JSONField(default=list)),
                ('age_from', models.CharField(blank=True, max_length=100, null=True)),
                ('age_to', models.CharField(blank=True, max_length=100, null=True)),
                ('experience', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('online_payment', models.TextField(blank=True, null=True)),
                ('keywords', models.CharField(blank=True, max_length=255, null=True)),
                ('clinic_name_or_service_email', models.CharField(blank=True, max_length=255, null=True)),
                ('service_address', models.CharField(blank=True, max_length=255, null=True)),
                ('appointment_time', models.CharField(blank=True, max_length=100, null=True)),
                ('home_service', models.TextField(blank=True, null=True)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('registration_time', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('specialty', models.CharField(blank=True, max_length=200)),
                ('institution', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]