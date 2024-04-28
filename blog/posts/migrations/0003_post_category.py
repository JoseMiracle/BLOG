# Generated by Django 5.0.4 on 2024-04-27 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_postreaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('travel', 'Travel'), ('food_cooking', 'Food and Cooking'), ('health_wellness', 'Health and Wellness'), ('lifestyle', 'Lifestyle'), ('education', 'Education')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
