# Generated by Django 4.2.1 on 2023-06-19 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0002_initial'),
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='review',
            name='review_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_profiles.profile'),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('review_owner', 'project')},
        ),
    ]
