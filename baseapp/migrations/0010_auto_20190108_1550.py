# Generated by Django 2.1.4 on 2019-01-08 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0009_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
