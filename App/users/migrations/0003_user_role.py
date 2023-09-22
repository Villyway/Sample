# Generated by Django 4.2 on 2023-08-22 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('SUPER_ADMIN', 'SUPER_ADMIN'), ('MANAGER', 'MANAGER'), ('OPERATOR', 'OPERATOR'), ('CUSTOMER', 'CUSTOMER')], default='CUSTOMER', max_length=25),
        ),
    ]
