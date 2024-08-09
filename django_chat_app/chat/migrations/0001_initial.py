# Generated by Django 5.1 on 2024-08-09 14:29

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField(max_length=500)),
                ('created_ad', models.DateField(default=datetime.date.today)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_message_set', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_message_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
