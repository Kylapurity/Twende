# Generated by Django 4.2.7 on 2024-07-08 18:05

from django.db import migrations, models
import safari_learning.models


class Migration(migrations.Migration):

    dependencies = [
        ('safari_learning', '0003_event_bookedevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='safariuser',
            name='age',
            field=models.PositiveSmallIntegerField(null=True, validators=[safari_learning.models.validate_age]),
        ),
    ]
