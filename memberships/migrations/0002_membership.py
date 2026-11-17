import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('frozen_until', models.DateField(blank=True, null=True)),
                ('last_action', models.CharField(choices=[('SUBSCRIBE', 'Subscribe'), ('RENEW', 'Renew'), ('FREEZE', 'Freeze')], default='SUBSCRIBE', max_length=10)),
                ('member', models.OneToOneField(limit_choices_to={'role': 'MEMBER'}, on_delete=django.db.models.deletion.CASCADE, related_name='membership', to=settings.AUTH_USER_MODEL)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='memberships', to='memberships.membershipplan')),
            ],
            options={
                'ordering': ['end_date'],
            },
        ),
    ]