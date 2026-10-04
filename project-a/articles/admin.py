from django.contrib import admin

from .models import Article, Attachment, AuditLog

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0
    fields = ["filename", "file", "thumbnail", "downloads", "uploaded_at"]
    readonly_fields = ["downloads", "uploaded_at"]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "status", "views", "is_deleted", "created_at"]
    list_filter = ["status", "is_deleted", "created_at"]
    search_fields = ["title", "body"]
    inlines = [AttachmentInline]

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["filename", "article", "downloads", "uploaded_at"]
    list_filter = ["uploaded_at"]

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "action", "article", "user"]
    list_filter = ["action", "timestamp"]
    search_fields = ["changes"]
    readonly_fields = ["article", "user", "action", "changes", "timestamp"]

    def has_add_permission(self, request):
        return False
