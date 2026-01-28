from piccolo.table import Table
from piccolo.columns import UUID, Varchar, Boolean


class Users(Table):
    id = UUID(primary_key=True)
    username = Varchar(length=100)
    full_name = Varchar(length=100)
    email = Varchar(length=200)
    hashed_password = Varchar(length=512)
    disabled = Boolean
