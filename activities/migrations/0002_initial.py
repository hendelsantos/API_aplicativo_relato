# Generated by Django 5.2.4 on 2025-07-13 12:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('activities', '0001_initial'),
        ('parts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenanceactivity',
            name='technician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Técnico'),
        ),
        migrations.AddField(
            model_name='activityphoto',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='activities.maintenanceactivity'),
        ),
        migrations.AddField(
            model_name='activityanswer',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='activities.maintenanceactivity'),
        ),
        migrations.AddField(
            model_name='partusage',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts_used', to='activities.maintenanceactivity'),
        ),
        migrations.AddField(
            model_name='partusage',
            name='part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parts.part', verbose_name='Peça'),
        ),
        migrations.AddField(
            model_name='standardquestion',
            name='activity_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='activities.activitytype'),
        ),
        migrations.AddField(
            model_name='activityanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.standardquestion', verbose_name='Pergunta'),
        ),
        migrations.AlterUniqueTogether(
            name='partusage',
            unique_together={('activity', 'part')},
        ),
        migrations.AlterUniqueTogether(
            name='activityanswer',
            unique_together={('activity', 'question')},
        ),
    ]
