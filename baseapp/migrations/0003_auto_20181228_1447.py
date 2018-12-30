# Generated by Django 2.1.4 on 2018-12-28 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0002_auto_20181226_1348'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='game',
            name='logo',
            field=models.ImageField(blank=True, upload_to='game_images'),
        ),
    ]