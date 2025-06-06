# Generated by Django 5.2 on 2025-04-30 01:47

import CampusMart.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CampusMart', '0007_userextralistings'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextralistings',
            name='extra_listings',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userextralistings',
            name='user',
            field=models.ForeignKey(default=CampusMart.models.get_default_user, on_delete=django.db.models.deletion.CASCADE, to='CampusMart.user'),
        ),
    ]
