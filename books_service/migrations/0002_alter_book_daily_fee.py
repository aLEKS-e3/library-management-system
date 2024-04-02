from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books_service", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="daily_fee",
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
