# Generated by Django 3.2.24 on 2024-11-28 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyc', '0013_auto_20241127_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessowner',
            name='encrypted_bvn',
            field=models.TextField(default=None),
        ),
    ]
