# Generated by Django 5.1.7 on 2025-04-06 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0013_comment_reported'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='reported',
            field=models.BooleanField(default=False),
        ),
    ]
