# myapp/cron.py
from .sub_email import send_reminder_emails, determine_sequence_logic

def email_scheduled_job():
    # 假设你有逻辑来确定current_sequence
    current_sequence = determine_sequence_logic()
    send_reminder_emails(current_sequence)
