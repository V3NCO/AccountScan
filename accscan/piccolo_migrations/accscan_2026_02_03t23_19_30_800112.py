from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text

ID = "2026-02-03T23:19:30:800112"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accscan", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="delivered_to",
        db_column_name="delivered_to",
        params={"null": True},
        old_params={"null": False},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="reply_to",
        db_column_name="reply_to",
        params={"null": True},
        old_params={"null": False},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    return manager
