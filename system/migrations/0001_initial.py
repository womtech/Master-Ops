# Generated by Django 2.1.7 on 2019-03-23 10:59

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import system.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('about', models.CharField(default='NA', max_length=65)),
                ('url', models.CharField(blank=True, default='#', max_length=20)),
                ('theme', models.CharField(blank=True, choices=[('A', 'default'), ('B', 'grey-bound'), ('C', 'metallic-shore'), ('D', 'red'), ('E', 'browny'), ('F', 'sky-lurk'), ('G', 'oceanic-blue')], max_length=2)),
                ('status', models.CharField(choices=[('AC', 'Active'), ('UM', 'Under Maintenance'), ('NA', 'Not Available')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='App_Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_verbose', models.CharField(max_length=80, verbose_name='Form Name')),
                ('form_name_html', models.CharField(max_length=40, verbose_name='Form HTML-ID')),
                ('available_operations', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Available Operations')),
                ('search', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Search Fields')),
                ('filter', django.contrib.postgres.fields.jsonb.JSONField(verbose_name='Filter Fields')),
                ('lv_fields', django.contrib.postgres.fields.jsonb.JSONField(blank=True, verbose_name='Form Fields')),
                ('is_active', models.BooleanField(default=True)),
                ('app_id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.App', verbose_name='Select App')),
            ],
            options={
                'verbose_name': 'App Form',
                'verbose_name_plural': 'App Forms',
            },
        ),
        migrations.CreateModel(
            name='Apps_Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_name', models.CharField(blank=True, default='No Name', max_length=60)),
                ('menus', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default='', verbose_name='Allowed Menus')),
                ('description', models.CharField(blank=True, max_length=250, verbose_name='Profile Description')),
                ('app_id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='system.App', verbose_name='Select App')),
                ('user_id_fk', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Select User')),
            ],
            options={
                'verbose_name': 'Apps Assignment',
                'verbose_name_plural': 'Apps Assignment',
            },
        ),
        migrations.CreateModel(
            name='User_Form_Level_Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=system.models.User_Form_Level_Permission.get_autogenerated_code, editable=False, max_length=8)),
                ('form_url', models.CharField(default='', max_length=30, verbose_name='Form URL')),
                ('permission_str', django.contrib.postgres.fields.jsonb.JSONField(default={'field_mapping': {'field_1': 'read-only', 'field_2': 'hidden', 'field_3': 'editable'}}, verbose_name='Permission String')),
                ('available_operations', django.contrib.postgres.fields.jsonb.JSONField(default=['select', 'delete', 'update', 'add'], verbose_name='Allowed Operations')),
                ('search', django.contrib.postgres.fields.jsonb.JSONField(default={'search': ['field_id_1', 'field_id_2']}, verbose_name='Allowed Search')),
                ('filter', django.contrib.postgres.fields.jsonb.JSONField(default={'filter': ['field_id_1', 'field_id_2']}, verbose_name='Allowed Filter')),
                ('app_assignment_id_fk', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.Apps_Assignment', verbose_name='Choose Apps Assignment')),
                ('form_id_fk', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='system.App_Form', verbose_name='Select Form')),
            ],
        ),
    ]
