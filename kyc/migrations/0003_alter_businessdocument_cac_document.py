# Generated by Django 3.2.24 on 2024-11-19 23:20

from django.db import migrations, models
import utility.validator


class Migration(migrations.Migration):

    dependencies = [
        ('kyc', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessdocument',
            name='cac_document',
            field=models.FileField(upload_to='kyc_documents/', validators=[utility.validator.validate_file_type]),
        ),
    ]