# myapp/cron.py
from .sub_email import send_reminder_emails, determine_sequence_logic

def email_scheduled_job():
    current_sequence = determine_sequence_logic()
    send_reminder_emails(current_sequence)
