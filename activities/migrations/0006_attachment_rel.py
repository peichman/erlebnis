# Generated by Django 4.0.6 on 2022-08-24 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_attachment_media_type_alter_attachment_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='rel',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]
