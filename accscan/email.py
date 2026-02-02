from accscan.tables import EmailAccounts
from accscan.utils import get_uuid
import imaplib

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
        conn.select()


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
