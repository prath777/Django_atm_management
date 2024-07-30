# Generated by Django 5.0.7 on 2024-07-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_user_deposit_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='deposit_amount',
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit_amount', models.FloatField(max_length=20)),
                ('withdraw_amount', models.FloatField(max_length=20)),
            ],
            options={
                'indexes': [models.Index(fields=['deposit_amount', 'withdraw_amount'], name='user_transa_deposit_38fa3d_idx')],
            },
        ),
    ]
