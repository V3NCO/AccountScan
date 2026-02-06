from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.table import Table
from piccolo.columns import UUID, Varchar, Boolean, Text, Timestamp


class Users(Table):
    id = UUID(primary_key=True)
    username = Varchar(length=100)
    public_key = Varchar(length=512)
    hashed_password = Varchar(length=512)
    disabled = Boolean

class EmailAccounts(Table):
    id = UUID(primary_key=True, null=False)
    user = Varchar(length=100, null=False)
    hostname = Varchar(length=200, null=False)
    username = Varchar(length=200, null=False)
    password = Varchar(length=200, null=False)
    secure = Boolean(null=False)

class Emails(Table):
    account = UUID(null=False)
    raw_message_base64 = Text(null=True)
    added_at = Timestamp(TimestampNow())
