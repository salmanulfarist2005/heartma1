# Generated by Django 5.0.4 on 2024-05-07 05:13

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_testimonial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='blog')),
                ('detiail_image', models.ImageField(upload_to='blog_/detail')),
                ('date', models.DateField(blank=True, null=True)),
                ('description', tinymce.models.HTMLField()),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]
