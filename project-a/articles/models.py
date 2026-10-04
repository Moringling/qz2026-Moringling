import os.path

from django.conf import settings
from django.db import models
from django.db.models import Model

def attachment_upload_path(instance, filename):
    return os.path.join("attachments", str(instance.article.id), filename)

def thumbnail_upload_path(instance, filename):
    return os.path.join("thumbnails", filename)

class Article(Model):
    class Status(models.TextChoices):
        DRAFT = "草稿"
        PUBLISHED = "已发布"
        ARCHIVED = "已归档"

    title = models.CharField("标题", max_length=200)
    body = models.TextField("正文")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles", verbose_name="作者")
    status = models.CharField("状态", max_length=15, choices=Status.choices, default=Status.DRAFT)
    views = models.PositiveIntegerField("浏览量", default=0)
    is_deleted = models.BooleanField("已删除",default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "文章"
        verbose_name_plural = "文章"

    def __str__(self) -> str:
        return self.title

class Attachment(Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="attachments", verbose_name="文章")
    filename = models.CharField("文件名", max_length=255)
    file = models.FileField("文件", upload_to=attachment_upload_path)
    thumbnail = models.ImageField("缩略图", upload_to=thumbnail_upload_path, blank=True,null=True)
    uploaded_at = models.DateTimeField("上传时间", auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "附件"
        verbose_name_plural = "附件"

    def __str__(self) -> str:
        return self.filename

class AuditLog(Model):
    class Action(models.TextChoices):
        CREATE = "create"
        UPDATE = "update"
        PUBLISH = "publish"
        ARCHIVE = "archive"
        DELETE = "delete"

    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs", verbose_name="文章")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs", verbose_name="操作用户")
    action = models.CharField("操作类型", max_length=15, choices=Action.choices)
    changes = models.JSONField("变更摘要",default=dict, blank=True)
    timestamp = models.DateTimeField("时间戳", auto_now_add=True)

    class Meta:
        ordering = ["-timestamp", "-id"]
        verbose_name = "审计日志"
        verbose_name_plural = "审计日志"

    def __str__(self) -> str:
        return f"[{self.timestamp:%Y-%m-%d %H-%M-%S}] {str(self.action)} by {str(self.user)}"