# Generated by Django 3.2.24 on 2024-11-27 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kyc', '0011_rename_accoun_number_bankaccount_account_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='KYC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('in_progress', 'In progress'), ('completed', 'Completed')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='businessdocument',
            name='cac_reg_number',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='KYCStatus',
        ),
    ]
