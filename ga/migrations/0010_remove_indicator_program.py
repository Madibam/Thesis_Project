# Generated by Django 2.0.1 on 2018-03-05 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ga', '0009_auto_20180305_0129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='indicator',
            name='program',
        ),
    ]
