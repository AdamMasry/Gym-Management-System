import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainerAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now=True)),
                ('member', models.OneToOneField(limit_choices_to={'role': 'MEMBER'}, on_delete=django.db.models.deletion.CASCADE, related_name='trainer_assignment', to=settings.AUTH_USER_MODEL)),
                ('trainer', models.ForeignKey(limit_choices_to={'role': 'TRAINER'}, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_members', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialty', models.CharField(max_length=100)),
                ('bio', models.TextField(blank=True)),
                ('user', models.OneToOneField(limit_choices_to={'role': 'TRAINER'}, on_delete=django.db.models.deletion.CASCADE, related_name='trainer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
