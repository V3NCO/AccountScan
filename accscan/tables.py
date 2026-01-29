from piccolo.table import Table
from piccolo.columns import UUID, Varchar, Boolean


class Users(Table):
    id = UUID(primary_key=True)
    username = Varchar(length=100)
    public_key = Varchar(length=512)
    email = Varchar(length=200)
    hashed_password = Varchar(length=512)
    disabled = Boolean
