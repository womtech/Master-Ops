# Generated by Django 2.1.7 on 2019-03-23 10:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='channel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('channel_id', models.CharField(max_length=100)),
                ('channel_name', models.CharField(max_length=100)),
                ('is_Affiliate_Channel', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('remarks', models.TextField(blank=True, default=True)),
            ],
            options={
                'verbose_name': 'Youtube Channel',
                'verbose_name_plural': 'Youtube Channels',
            },
        ),
        migrations.CreateModel(
            name='cms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cms_id', models.CharField(max_length=100)),
                ('cms_name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Youtube CMS',
                'verbose_name_plural': 'Youtube CMS(s)',
            },
        ),
        migrations.CreateModel(
            name='facebook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('page_id', models.CharField(max_length=100)),
                ('page_name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('catagory', models.CharField(blank=True, choices=[('AM', 'Arts_Marketing'), ('EP', 'Event_Planning')], max_length=2)),
                ('sub_catagory', models.CharField(blank=True, choices=[('P', 'Publisher'), ('DJ', 'DJ')], max_length=2)),
                ('tags', models.TextField(blank=True, default=True)),
                ('description', models.TextField(blank=True, default=True)),
                ('remarks', models.TextField(blank=True, default=False)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Facebook Page',
                'verbose_name_plural': 'Facebook Pages',
            },
        ),
        migrations.CreateModel(
            name='instagram',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('handle', models.CharField(max_length=100)),
                ('account_name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('catagory', models.CharField(blank=True, choices=[('AM', 'Arts Marketing'), ('EP', 'Event Planning')], max_length=2)),
                ('description', models.TextField(blank=True, default=True)),
                ('remarks', models.TextField(blank=True, default=False)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Instagram Account',
                'verbose_name_plural': 'Instagram Accounts',
            },
        ),
        migrations.CreateModel(
            name='twitter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('handle', models.CharField(max_length=100)),
                ('account_name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('catagory', models.CharField(blank=True, choices=[('AM', 'Arts Marketing'), ('EP', 'Event Planning')], max_length=2)),
                ('description', models.TextField(blank=True, default=True)),
                ('remarks', models.TextField(blank=True, default=False)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Twitter Handle',
                'verbose_name_plural': 'Twitter Handles',
            },
        ),
        migrations.CreateModel(
            name='youtube_videos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('video_id', models.CharField(max_length=30, verbose_name='Video ID As In Youtube')),
                ('video_title', models.CharField(max_length=250, verbose_name='Video Title')),
                ('thumbnail', models.CharField(blank=True, default='', max_length=50, verbose_name='Thumbnail URL')),
                ('video_description', models.TextField(default=False, verbose_name='Video Description')),
                ('video_tags', models.TextField(default=False, verbose_name='Video Tags')),
                ('video_status', models.CharField(choices=[('PR', 'private'), ('PB', 'public'), ('PL', 'published')], max_length=2, verbose_name='Video Status')),
                ('video_published_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Video Published Time')),
                ('spam_level', models.CharField(blank=True, choices=[('NA', 'None'), ('TN', 'Thumbnail'), ('MT', 'Meta'), ('CM', 'Comma'), ('ML', 'Multiple')], default='NA', max_length=2)),
                ('qc_action', models.BooleanField(blank=True, default=False)),
                ('channel_id_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.channel', verbose_name='Select Channel')),
            ],
            options={
                'verbose_name': 'Youtube Video',
                'verbose_name_plural': 'Youtube Videos',
            },
        ),
        migrations.AddField(
            model_name='channel',
            name='cms_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.cms'),
        ),
    ]
