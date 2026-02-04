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
    email_from = Text(null=True)
    email_to = Text(null=True)
    delivered_to = Text(null=True)
    subject = Text(null=True)
    reply_to = Text(null=True)
    body = Text(null=True)
    added_at = Timestamp(TimestampNow())
