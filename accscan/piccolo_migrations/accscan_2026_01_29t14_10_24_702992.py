from piccolo.apps.migrations.auto.migration_manager import MigrationManager

ID = "2026-01-29T14:10:24:702992"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accscan", description=DESCRIPTION
    )

    manager.rename_column(
        table_class_name="Users",
        tablename="users",
        old_column_name="full_name",
        new_column_name="public_key",
        old_db_column_name="full_name",
        new_db_column_name="public_key",
        schema=None,
    )

    return manager
