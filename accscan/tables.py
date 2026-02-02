from piccolo.table import Table
from piccolo.columns import UUID, Varchar, Boolean


class Users(Table):
    id = UUID(primary_key=True)
    username = Varchar(length=100)
    public_key = Varchar(length=512)
    hashed_password = Varchar(length=512)
    disabled = Boolean

class EmailAccounts(Table):
    id = UUID(primary_key=True)
    user = Varchar(length=100)
    hostname = Varchar(length=200)
    username = Varchar(length=200)
    password = Varchar(length=200)
    secure = Boolean()
