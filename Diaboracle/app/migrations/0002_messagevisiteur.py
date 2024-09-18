# Generated by Django 5.1 on 2024-08-30 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageVisiteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('telephone', models.CharField(max_length=100)),
                ('sujet', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
