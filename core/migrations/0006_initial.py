# Generated by Django 4.1.7 on 2023-04-23 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0005_delete_media'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user', models.TextField()),
                ('video', models.FileField(blank=True, null=True, upload_to='video')),
                ('audio', models.FileField(blank=True, null=True, upload_to='audio')),
                ('text', models.FileField(blank=True, null=True, upload_to='text')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
