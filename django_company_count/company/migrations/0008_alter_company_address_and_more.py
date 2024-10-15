# Generated by Django 4.2.2 on 2024-10-12 18:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0007_alter_company_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="address",
            field=models.TextField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="current_employee_estimate",
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="domain",
            field=models.CharField(
                blank=True, db_index=True, max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="industry",
            field=models.CharField(
                blank=True, db_index=True, max_length=255, null=True
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="name",
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="company",
            name="size_range",
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="total_employee_estimate",
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
