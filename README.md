# AccountScan

## How does this work ?
The scan system should separate the emails into 5 categories: 
- Newsletter
- Spam/Phishing...
- Account emails
- Receipts
- Normal/Personal/Other emails

This will be based on a score system, each hint towards one type of email will give points;
For example, if we see "List-Unsubscribe" on an email- I'm going to attribute a lot of points towards a Newsletter email, because it's a fairly high confidence clue towards it being a Newsletter email.

Here are the quickest checks i'm going to perform, and the points assigned (going to make them up on the spot): 
- Check list-Unsubscribe = 100 Points for Newsletter
- Typical Keywords such as "Reset Password", "Verify Email"... = 65 Points for Account email
- Typical Keywords such as "Newsletter", "Digest"... = 65 Points for Newsletter
- DKIM/SPF failure = 50 Points towards Spam/Phishing Emails
- If from common mailing service (mailchimp, sendgrid, campaign-monitor, mailersend, resend) = 25 Points towards both Newsletter, Receipts, Account Emails
There are more checks like this that I'm going to perform to be able to identify email types, and when I'm unsure i'll probably run an AI model on it (still unsure what or how) to find out the right type.

Once this is done- the system will check for info about each email that isn't a personal email, like platform name, sender ect to be able to return the info to the user.
