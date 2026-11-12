import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='MembershipPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('duration_days', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.01'), message='Price must be greater than zero.')])),
                ('is_active', models.BooleanField(default=True, help_text='Only active plans are shown to members.')),
            ],
            options={
                'ordering': ['price', 'name'],
            },
        ),
    ]
