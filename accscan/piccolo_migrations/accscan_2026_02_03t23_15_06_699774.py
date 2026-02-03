from piccolo.apps.migrations.auto.migration_manager import MigrationManager

ID = "2026-02-03T23:15:06:699774"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accscan", description=DESCRIPTION
    )

    manager.drop_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="date",
        db_column_name="date",
        schema=None,
    )

    return manager
