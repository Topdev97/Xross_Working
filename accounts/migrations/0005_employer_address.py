# Generated by Django 4.0.6 on 2023-05-31 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_userskill_skill_remove_userskill_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='address',
            field=models.CharField(default='', max_length=500),
        ),
    ]