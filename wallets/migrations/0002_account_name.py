# Generated by Django 4.1.4 on 2023-01-02 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
