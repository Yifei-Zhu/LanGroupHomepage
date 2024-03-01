from django.contrib import admin
from .models import DutyGroup

class DutyGroupAdmin(admin.ModelAdmin):
    # list_display = ('name', 'sequence')  # 显示组名和序列号
    list_display = ('num',)  # 显示组名和序列号
    filter_horizontal = ('users',)  # 使得用户字段在界面中更易于编辑
    ordering = ('num',)  # 根据序列号排序
    search_fields = ('num',)  # 允许通过组名搜索

admin.site.register(DutyGroup, DutyGroupAdmin)
