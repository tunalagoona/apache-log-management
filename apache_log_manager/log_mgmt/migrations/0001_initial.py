# Generated by Django 3.2 on 2021-04-22 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApacheLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=200, verbose_name='IP address')),
                ('log_date', models.DateTimeField(db_index=True, default=None, verbose_name='Log date')),
                ('HTTP_method', models.CharField(db_index=True, max_length=200)),
                ('URI', models.CharField(max_length=700)),
                ('response_code', models.IntegerField(db_index=True, verbose_name='Response code')),
                ('response_size', models.CharField(max_length=200)),
                ('referer', models.CharField(default=None, max_length=400, verbose_name='Referer')),
                ('user_agent', models.CharField(default=None, max_length=400, verbose_name='User Agent')),
            ],
        ),
    ]
