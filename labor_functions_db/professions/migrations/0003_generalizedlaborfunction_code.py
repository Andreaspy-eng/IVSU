# Generated by Django 5.1.6 on 2025-02-23 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('professions', '0002_alter_laborfunction_generalized_function'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalizedlaborfunction',
            name='code',
            field=models.CharField(default='TEMP_CODE', max_length=20, unique=True),
        ),
    ]
