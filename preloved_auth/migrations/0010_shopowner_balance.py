# Generated by Django 4.2.7 on 2023-12-06 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preloved_auth', '0009_alter_staff_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopowner',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]