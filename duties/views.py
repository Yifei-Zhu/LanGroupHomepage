from django.shortcuts import render
from .models import DutyGroup

def show_groups(request):
    groups = DutyGroup.objects.all()  # 获取所有组
    return render(request, 'groups/show_groups.html', {'groups': groups})
