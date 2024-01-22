from django.contrib import admin
from django.utils.html import format_html
from letterapp.models import Letter



class LetterAdmin(admin.ModelAdmin):
    def display_letter(self, obj):
        return f"[{obj.writer}] {obj.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    display_letter.short_description = '편지 정보'
    list_display = ('display_letter',)
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    fields = ('display_letter_info',)
    readonly_fields = ('display_letter_info',)


    def display_letter_info(self, obj):
        letter_title= obj.letter_info.title if obj.letter_info.title else '제목 없음'
        letter_finished_at= obj.finished_at.strftime('%Y-%m-%d %H:%M:%S') if obj.finished_at else '미완료'
        return format_html(
            "<strong>제목:</strong> {}<br>"
            "<strong>작성자:</strong> {}<br>"
            "<strong>수신자:</strong> {}<br>"
            "<strong> </strong> {}<br>"
            "<strong>작성 완료 시간:</strong> {}<br>"
            "<strong>작성 일시:</strong> {}<br>"
            "<strong>작성 단계:</strong> {}<br>"
            "<strong>확인 단계:</strong> {}"
            "<strong>URL:</strong> {}",
            letter_title,
            obj.writer,
            obj.saver,
            ' ',
            letter_finished_at,
            obj.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            obj.progress,
            obj.state,
            obj.url,
        )
    display_letter_info.short_description = '편지 정보'



admin.site.register(Letter, LetterAdmin)