# Generated by Django 5.0.3 on 2024-04-01 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0003_alter_borrowing_book_id_alter_borrowing_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
