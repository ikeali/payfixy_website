# Generated by Django 3.2.24 on 2024-11-26 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kyc', '0010_bankaccount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bankaccount',
            old_name='accoun_number',
            new_name='account_number',
        ),
    ]