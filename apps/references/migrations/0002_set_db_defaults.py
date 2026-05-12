# apps/references/migrations/0002_set_db_defaults.py
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('references', '0001_initial'),  # 👈 Убедись, что имя совпадает с твоей первой миграцией
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE references_enginemodel ALTER COLUMN created_at SET DEFAULT NOW();
            ALTER TABLE references_enginemodel ALTER COLUMN updated_at SET DEFAULT NOW();

            ALTER TABLE references_transmissionmodel ALTER COLUMN created_at SET DEFAULT NOW();
            ALTER TABLE references_transmissionmodel ALTER COLUMN updated_at SET DEFAULT NOW();

            ALTER TABLE references_drivingaxlemodel ALTER COLUMN created_at SET DEFAULT NOW();
            ALTER TABLE references_drivingaxlemodel ALTER COLUMN updated_at SET DEFAULT NOW();

            ALTER TABLE references_steerableaxlemodel ALTER COLUMN created_at SET DEFAULT NOW();
            ALTER TABLE references_steerableaxlemodel ALTER COLUMN updated_at SET DEFAULT NOW();

            ALTER TABLE references_techniquemodel ALTER COLUMN created_at SET DEFAULT NOW();
            ALTER TABLE references_techniquemodel ALTER COLUMN updated_at SET DEFAULT NOW();

            ALTER TABLE references_maintenancetype ALTER COLUMN created_at SET DEFAULT NOW();
            ALTER TABLE references_maintenancetype ALTER COLUMN updated_at SET DEFAULT NOW();
            """,
            reverse_sql="SELECT 1;"  # Безопасная заглушка для отката
        ),
    ]