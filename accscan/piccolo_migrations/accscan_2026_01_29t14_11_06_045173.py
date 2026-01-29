from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar

ID = "2026-01-29T14:11:06:045173"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accscan", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Users",
        tablename="users",
        column_name="public_key",
        db_column_name="public_key",
        params={"length": 512},
        old_params={"length": 100},
        column_class=Varchar,
        old_column_class=Varchar,
        schema=None,
    )

    return manager
