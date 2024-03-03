from django.shortcuts import render
from .models import DutyGroup

def show_groups(request):
    groups = DutyGroup.objects.all()
    # 对每个组中的用户按姓氏排序
    for group in groups:
        group.sorted_users = group.users.all().order_by('last_name')
    return render(request, 'groups/show_groups.html', {'groups': groups})

