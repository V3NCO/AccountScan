from accscan.tables import EmailAccounts, Emails
from accscan.utils import get_uuid
import imaplib
import email
from email import policy
import uuid
import base64

async def add_user_email(
    current_user,
    hostname,
    username,
    password,
    secure
):
    if current_user & hostname & username & password & secure:
        try:
            if secure:
                conn = imaplib.IMAP4_SSL(hostname)
            else:
                conn = imaplib.IMAP4(hostname)
            conn.login(username, password)
            conn.select(readonly=True)


            await EmailAccounts.insert(EmailAccounts(
                id=await get_uuid(EmailAccounts, EmailAccounts.id),
                user=current_user.username,
                hostname=hostname,
                username=username,
                password=password,
                secure=secure
            ))
            return {"ok": True}
        except Exception as e:
            return {"ok": False, "error": f"Error: {e}"}
    else:
        return {"ok": False, "error": "All the fields need to be filled!"}

async def pull_all_emails(
    current_user
):
    # This deletes all emails for that account and then starts pulling
    # Why is that so unoptimized you say?
    # Because I cannot be bothered to find a way for my email puller
    # to know exactly which mail it already has or not
    accounts = await EmailAccounts.select().where(EmailAccounts.user == current_user.username)
    for account in accounts:
        if account['secure']:
            conn = imaplib.IMAP4_SSL(account['hostname'])
        else:
            conn = imaplib.IMAP4(account['hostname'])
        conn.login(account['username'], account['password'])
        status, messages = conn.select(readonly=True)

        if status != "OK":
            return {"ok": False, "error": "Incorrect mail box"}
        else:
            await Emails.delete().where(Emails.account == account["id"])
            for i in range(1, int(messages[0])): #type:ignore i have no idea how to fix th
                res, messages = conn.fetch(str(i), '(RFC822)')
                for response in messages:
                    if isinstance(response, tuple):
                        raw_bytes = response[1]
                        if raw_bytes is None:
                            continue
                        b64_bytes = base64.b64encode(raw_bytes)
                        b64_str = b64_bytes.decode('ascii')
                        await Emails.insert(
                            Emails(
                                account = account["id"],
                                raw_message_base64 = b64_str,
                            )
                        )

async def pull_emails(
    current_user,
    account_id
):
    if await validate_uuid(account_id):
        account_db = await EmailAccounts.select().where(EmailAccounts.id == account_id)
        account = account_db[0]
        if account['secure']:
            conn = imaplib.IMAP4_SSL(account['hostname'])
        else:
            conn = imaplib.IMAP4(account['hostname'])
        conn.login(account['username'], account['password'])
        status, messages = conn.select(readonly=True)

        if status != "OK":
            return {"ok": False, "error": "Incorrect mail box"}
        else:
            await Emails.delete().where(Emails.account == account["id"])
            for i in range(1, int(messages[0])): #type:ignore i have no idea how to fix th
                res, messages = conn.fetch(str(i), '(RFC822)')
                for response in messages:
                    if isinstance(response, tuple):
                        raw_bytes = response[1]
                        if raw_bytes is None:
                            continue
                        b64_bytes = base64.b64encode(raw_bytes)
                        b64_str = b64_bytes.decode('ascii')
                        await Emails.insert(
                            Emails(
                                account = account["id"],
                                raw_message_base64 = b64_str,
                            )
                        )

async def decode_dbmail(raw_b64: str):
    if isinstance(raw_b64, str):
        b64_bytes = raw_b64.encode('ascii')
    else:
        b64_bytes = raw_b64

    raw_bytes = base64.b64decode(b64_bytes)
    msg = email.message_from_bytes(raw_bytes, policy=policy.default)
    return msg

async def get_email_body(msg):
    if msg.is_multipart():
        part = msg.get_body(preferencelist=('plain', 'html'))
        if part:
            body_text = part.get_content()
        else:
            body_text = ''.join(p.get_content() for p in msg.iter_parts() if p.get_content_type().startswith('text/'))
    else:
        body_text = msg.get_content()
    return body_text


async def validate_uuid(test, version=4):
    try:
       uuid.UUID(test, version=version)
    except ValueError:
        return False
    return True


async def check_progress(
    current_user,
    account
):
    if await validate_uuid(account):
        dbline = await EmailAccounts.select().where(EmailAccounts.id == account)
        creds = dbline[0]
        if creds["user"] == current_user.username:
            if creds['secure']:
                conn = imaplib.IMAP4_SSL(creds['hostname'])
            else:
                conn = imaplib.IMAP4(creds['hostname'])
            conn.login(creds['username'], creds['password'])
            status, messages = conn.select(readonly=True)
            dbcount = await Emails.count().where(Emails.account == account)
            return {"ok": True,"indb": dbcount, "inbox":int(messages[0].decode())-1} #type:ignore
        else:
            return {"ok": False, "error": "This address is not assigned to your account!"}
    else:
        return {"ok": False, "error": "Not a valid UUID!"}


async def list_user_email(
    current_user
):
    dblines = await EmailAccounts.select(EmailAccounts.id, EmailAccounts.username, EmailAccounts.hostname, EmailAccounts.secure).where(EmailAccounts.user == current_user.username)
    return dblines

async def delete_email(
    current_user,
    account_id,
    rm_user: bool = False
):
    if await validate_uuid(account_id):
        dbline = await EmailAccounts.select().where(EmailAccounts.id == account_id)
        creds = dbline[0]
        if creds["user"] == current_user.username:
            await Emails.delete().where(Emails.account == account_id)
            if rm_user:
                await EmailAccounts.delete().where(EmailAccounts.id == account_id)
            return {"ok": True}
        else:
            return {"ok": False, "error": "This address is not assigned to your account!"}
    else:
        return {"ok": False, "error": "Not a valid UUID!"}
