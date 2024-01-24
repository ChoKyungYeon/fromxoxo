from django.contrib import admin
from django.utils.html import format_html
from .models import Analytics


class AnalyticsAdmin(admin.ModelAdmin):
    def display_analytics(self, obj):
        return f"[{obj.created_at}] 방문 {obj.view_count}/ 신규 가입 {obj.user_count()}/ 편지 작성 {obj.letter_count}"
    display_analytics.short_description = '활동 통계'

    list_display = ('display_analytics',)
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    fields = ('display_analytics_info',)
    readonly_fields = ('display_analytics_info',)

    def display_analytics_info(self, obj):
        return format_html(
            "<strong>통계 일시:</strong> {}<br>"
            "<strong>방문자 수:</strong> {}<br>"
            "<strong>신규 가입:</strong> {}<br>"
            "<strong>편지 작성:</strong> {}<br>",
            obj.created_at,
            obj.view_count,
            obj.user_count(),
            obj.letter_count,

        )

    display_analytics_info.short_description = '편지 정보'


admin.site.register(Analytics, AnalyticsAdmin)