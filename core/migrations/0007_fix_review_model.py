from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_alter_master_options_alter_order_options_and_more'),
    ]

    operations = [
        # Удаляем таблицу core_review, если она существует
        migrations.RunSQL(
            "DROP TABLE IF EXISTS core_review;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
