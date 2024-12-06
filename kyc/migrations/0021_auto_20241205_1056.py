# Generated by Django 3.2.24 on 2024-12-05 18:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('kyc', '0020_alter_kyc_merchant'),
    ]

    operations = [
        migrations.RenameField(
            model_name='businessdetails',
            old_name='busienss_description',
            new_name='business_description',
        ),
        migrations.AddField(
            model_name='kyc',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='kyc',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]