from piccolo.apps.migrations.auto.migration_manager import MigrationManager

ID = "2026-01-28T15:24:18:797600"
VERSION = "1.30.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="", description=DESCRIPTION
    )

    def run():
        print(f"running {ID}")

    manager.add_raw(run)

    return manager
