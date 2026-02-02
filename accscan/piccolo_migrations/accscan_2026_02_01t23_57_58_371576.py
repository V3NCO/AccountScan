from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Varchar
from piccolo.columns.indexes import IndexMethod

ID = "2026-02-01T23:57:58:371576"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="accscan", description=DESCRIPTION
    )

    manager.rename_table(
        old_class_name="EmailAddresses",
        old_tablename="email_addresses",
        new_class_name="EmailAccounts",
        new_tablename="email_accounts",
        schema=None,
    )

    manager.drop_column(
        table_class_name="EmailAccounts",
        tablename="email_accounts",
        column_name="address",
        db_column_name="address",
        schema=None,
    )

    manager.add_column(
        table_class_name="EmailAccounts",
        tablename="email_accounts",
        column_name="hostname",
        db_column_name="hostname",
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

    manager.add_column(
        table_class_name="EmailAccounts",
        tablename="email_accounts",
        column_name="password",
        db_column_name="password",
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

    manager.add_column(
        table_class_name="EmailAccounts",
        tablename="email_accounts",
        column_name="username",
        db_column_name="username",
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

    return manager
