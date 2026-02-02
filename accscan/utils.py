import uuid
from piccolo.columns import UUID


async def get_uuid(table, id: UUID):
    uuidfound = False
    while not uuidfound:
        currentuuid = uuid.uuid4()
        if await table.exists().where(id == currentuuid):
            uuidfound = False
        else:
            uuidfound = True
            return currentuuid
