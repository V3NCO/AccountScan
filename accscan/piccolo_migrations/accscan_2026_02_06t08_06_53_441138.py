from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.indexes import IndexMethod

ID = "2026-02-06T08:06:53:441138"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accscan", description=DESCRIPTION
    )

    manager.drop_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="body",
        db_column_name="body",
        schema=None,
    )

    manager.drop_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="delivered_to",
        db_column_name="delivered_to",
        schema=None,
    )

    manager.drop_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="email_from",
        db_column_name="email_from",
        schema=None,
    )

    manager.drop_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="email_to",
        db_column_name="email_to",
        schema=None,
    )

    manager.drop_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="reply_to",
        db_column_name="reply_to",
        schema=None,
    )

    manager.drop_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="subject",
        db_column_name="subject",
        schema=None,
    )

    manager.add_column(
        table_class_name="Emails",
        tablename="emails",
        column_name="raw_message_base64",
        db_column_name="raw_message_base64",
        column_class_name="Text",
        column_class=Text,
        params={
            "default": "",
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    return manager
