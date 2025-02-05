from django.db import migrations

def load_sql_from_file(apps, schema_editor):
    with open('movies/sql/base_data.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    schema_editor.execute(sql)

class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_sql_from_file),
    ]
