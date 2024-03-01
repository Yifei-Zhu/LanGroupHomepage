from .models import DutyGroup

def get_next_groups(current_num):
    # 获取所有组，按num排序
    all_groups = list(DutyGroup.objects.all().order_by('num'))

    # 找到当前组的索引
    current_index = next((index for index, group in enumerate(all_groups) if group.num == current_num), None)

    if current_index is None:
        return None, None  # 当前序列不在列表中

    # 计算正序和倒序的下一个组的索引
    next_index = (current_index)
    prev_index = -(current_index+1)

    # 获取组
    next_group = all_groups[next_index]
    prev_group = all_groups[prev_index]

    return next_group, prev_group

def get_group_emails(group):
    return [user.email for user in group.users.all() if user.email]

def create_email_message(group):
    member_names = [f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else user.username for user in group.users.all()]
    members_list = ", ".join(member_names)
    message = f"Hi, you are on duty next week. Please be prepared. Your team members are: {members_list}."
    return message

from django.core.mail import send_mail

def send_email_to_group(group, subject):
    message = create_email_message(group)  # 创建包含成员信息的邮件正文
    for user in group.users.all():
        send_mail(
            subject,
            message,
            'lan_group@outlook.com',  # 发件人邮箱
            [user.email],  # 收件人邮箱列表
            fail_silently=False,
        )

def send_reminder_emails(current_sequence):
    next_group, prev_group = get_next_groups(current_sequence)

    if next_group:
        send_email_to_group(next_group, 'Next Week Duty Reminder - 507')

    if prev_group:
        send_email_to_group(prev_group, 'Next Week Duty Reminder - Lan\'s Office')

from datetime import datetime, date

def determine_sequence_logic():
    year_start = date(datetime.now().year, 3, 1)
    # 获取今天的日期
    today = date.today()
    today = date(datetime.now().year, 3, 10)
    # 计算今天是今年的第几周
    current_week = (today - year_start).days // 7 + 1

    # 获取组的总数
    total_groups = DutyGroup.objects.count()
    if total_groups == 0:
        return None  # 如果没有组，则返回None

    next_sequence = current_week % total_groups

    if next_sequence == 0:
        next_sequence = total_groups

    return next_sequence

def main():
    # 假设你有逻辑来确定current_sequence
    current_sequence = determine_sequence_logic()
    send_reminder_emails(current_sequence)
