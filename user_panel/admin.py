from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'id_number', 'avatar')
    search_fields = ('user__username', 'phone_number', 'id_number')

    # 禁止通过admin界面添加UserProfile
    def has_add_permission(self, request, obj=None):
        return False
    # 禁止通过admin界面删除UserProfile
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(UserProfile, UserProfileAdmin)

