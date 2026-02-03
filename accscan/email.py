from accscan.tables import EmailAccounts, Emails, Users
from accscan.utils import get_uuid
import imaplib
import email
from email import policy

async def add_user_email(
    current_user,
    hostname,
    username,
    password,
    secure
):
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

async def pull_emails(
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
            for i in range(1, int(messages[0])): #type:ignore i have no idea how to fix th
                res, messages = conn.fetch(str(i), '(RFC822)')
                for response in messages:
                    if isinstance(response, tuple):
                        msg = email.message_from_bytes(response[1], policy=policy.default)
                        if msg.is_multipart():
                            part = msg.get_body(preferencelist=('plain', 'html'))
                            if part:
                                body_text = part.get_content()
                            else:
                                body_text = ''.join(p.get_content() for p in msg.iter_parts() if p.get_content_type().startswith('text/'))
                        else:
                            body_text = msg.get_content()
                        await Emails.insert(
                            Emails(
                                account = account['id'],
                                email_from = msg["From"],
                                email_to = msg["To"],
                                delivered_to = msg["Delivered-To"],
                                subject = msg["Subject"],
                                reply_to = msg["Reply-To"],
                                body = body_text
                            )
                        )
