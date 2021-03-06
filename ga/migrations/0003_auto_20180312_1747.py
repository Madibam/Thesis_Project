# Generated by Django 2.0.1 on 2018-03-12 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ga', '0002_auto_20180312_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='assessmentMethod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ga.AssessmentMethod'),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ga.Program'),
        ),
    ]
