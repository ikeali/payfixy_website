# Generated by Django 3.2.24 on 2024-11-20 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kyc', '0005_remove_businessowner_upload_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessowner',
            name='date_of_birth',
            field=models.DateTimeField(),
        ),
    ]