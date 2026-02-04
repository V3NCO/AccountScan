from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text

ID = "2026-02-04T00:22:35:689565"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accscan", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="body",
        db_column_name="body",
        params={"null": True},
        old_params={"null": False},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="email_from",
        db_column_name="email_from",
        params={"null": True},
        old_params={"null": False},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="email_to",
        db_column_name="email_to",
        params={"null": True},
        old_params={"null": False},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    manager.alter_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="subject",
        db_column_name="subject",
        params={"null": True},
        old_params={"null": False},
        column_class=Text,
        old_column_class=Text,
        schema=None,
    )

    return manager
