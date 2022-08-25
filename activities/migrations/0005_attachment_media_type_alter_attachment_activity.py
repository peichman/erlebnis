# Generated by Django 4.0.6 on 2022-08-22 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0004_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='media_type',
            field=models.CharField(default='application/gpx+xml', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attachment',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='activities.activity'),
        ),
    ]