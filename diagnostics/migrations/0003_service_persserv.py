# Generated by Django 3.2.13 on 2024-07-20 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0002_service_emails'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='persServ',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
