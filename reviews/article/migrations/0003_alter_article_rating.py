# Generated by Django 5.1.1 on 2024-09-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_alter_article_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=3, null=True),
        ),
    ]
