# Generated by Django 5.0.2 on 2024-05-29 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='author_pseudonym',
            field=models.CharField(max_length=100, null=True),
        ),
    ]