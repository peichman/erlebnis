# Generated by Django 4.0.6 on 2022-08-14 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='actor',
            field=models.ManyToManyField(blank=True, to='activities.actor'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='end_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='location',
            field=models.ManyToManyField(blank=True, to='activities.place'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='start_time',
            field=models.DateTimeField(blank=True),
        ),
    ]