# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_purchaseorder_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=True, help_text='False jika member dinonaktifkan dan tidak bisa login', verbose_name='Aktif'),
        ),
    ]


