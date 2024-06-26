# Generated by Django 4.2.8 on 2024-01-02 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_item_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoadVoucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_code', models.CharField(max_length=20)),
                ('value', models.IntegerField()),
                ('is_redeemed', models.IntegerField(default=0)),
            ],
        ),
    ]
