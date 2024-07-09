# Generated by Django 4.2.7 on 2024-07-08 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('safari_learning', '0002_alter_safaricourse_course_tags_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(choices=[('Entrepreneurship and Ventures Masterclass', 'Entrepreneurship and Ventures Masterclass'), ('Wildlife Campaign Awareness', 'Wildlife Campaign Awareness'), ('Sustainable Futures Forum', 'Sustainable Futures Forum'), ('Wildlife Warriors Workshop', 'Wildlife Warriors Workshop'), ('Wildlife Conservation Symposium', 'Wildlife Conservation Symposium')], max_length=1000)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=1000)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookedEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('events', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='all_booking', to='safari_learning.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
