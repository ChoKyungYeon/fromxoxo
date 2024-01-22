from django.contrib import admin
from django.utils.html import format_html

from .models import CustomUser
from django.contrib.auth.models import Group


admin.site.unregister(Group)
admin.site.site_header = 'FromXoXo 유저 관리'
admin.site.index_title = ""


class CustomUserAdmin(admin.ModelAdmin):
    def display_user(self, obj):
        return f"[{obj.username}] {obj.phonenumber} {obj.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    display_user.short_description = '유저 활동 정보'
    list_display = ('display_user',)

    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    fields = ('display_user_info',)
    readonly_fields = ('display_user_info',)


    def display_user_info(self, obj):
        return format_html(
            "<strong>아이디:</strong> {}<br>"
            "<strong>연락처:</strong> {}<br>"
            "<strong>가입 일시:</strong> {}<br>"
            "<strong>작성 편지:</strong> {}<br>"
            "<strong>저장 편지:</strong> {}",
            obj.username,
            obj.phonenumber,
            obj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            obj.letter_writer.all().count(),
            obj.letter_saver.all().count(),
        )
    display_user_info.short_description = '사용자 정보'



admin.site.register(CustomUser, CustomUserAdmin)