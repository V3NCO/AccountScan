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
    id = UUID(primary_key=True)
    user = Varchar(length=100)
    hostname = Varchar(length=200)
    username = Varchar(length=200)
    password = Varchar(length=200)
    secure = Boolean()

class Emails(Table):
    account = UUID()
    email_from = Text()
    email_to = Text()
    delivered_to = Text()
    subject = Text()
    reply_to = Text()
    body = Text()
    added_at = Timestamp(TimestampNow())
