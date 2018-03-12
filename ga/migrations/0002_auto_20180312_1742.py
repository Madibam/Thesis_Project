# Generated by Django 2.0.1 on 2018-03-12 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ga', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='current_flag',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='assessment',
            name='assessmentMethod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ga.AssessmentMethod'),
        ),
    ]