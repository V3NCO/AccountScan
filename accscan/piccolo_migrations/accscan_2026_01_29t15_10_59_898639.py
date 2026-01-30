from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import UUID
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.uuid import UUID4
from piccolo.columns.indexes import IndexMethod

ID = "2026-01-29T15:10:59:898639"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accscan", description=DESCRIPTION
    )

    manager.add_table(
        class_name="EmailAddresses",
        tablename="email_addresses",
        schema=None,
        columns=None,
    )

    manager.add_column(
        table_class_name="EmailAddresses",
        tablename="email_addresses",
        column_name="id",
        db_column_name="id",
        column_class_name="UUID",
        column_class=UUID,
        params={
            "default": UUID4(),
            "null": False,
            "primary_key": True,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="EmailAddresses",
        tablename="email_addresses",
        column_name="user",
        db_column_name="user",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 100,
            "default": "",
            "null": False,
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

    manager.add_column(
        table_class_name="EmailAddresses",
        tablename="email_addresses",
        column_name="address",
        db_column_name="address",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 200,
            "default": "",
            "null": False,
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

    manager.drop_column(
        table_class_name="Users",
        tablename="users",
        column_name="email",
        db_column_name="email",
        schema=None,
    )

    return manager
