# Generated by Django 4.1.7 on 2023-02-27 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
