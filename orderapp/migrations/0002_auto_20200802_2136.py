# Generated by Django 2.2 on 2020-08-02 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orderapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='активен'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='mainapp.Product', verbose_name='продукт'),
        ),
    ]
