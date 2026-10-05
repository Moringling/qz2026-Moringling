from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch.dispatcher import receiver

from articles.middleware import get_current_user
from articles.models import Article, AuditLog

TRACKED_FIELDS = ("title", "body", "status", "is_deleted")

@receiver(pre_save, sender=Article)
def capture_old_article_state(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_state = None
        return
    try:
        instance._old_state = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        instance._old_state = None

def _diff(old, new):
    changes = {}
    for field in TRACKED_FIELDS:
        old_value = None if old is None else getattr(old, field)
        new_value = getattr(new, field)
        if old_value != new_value:
            changes[field] = {"old": old_value, "new": new_value}
    return changes

def _resolve_action(changes):
    status_change = changes.get("status")
    if status_change:
        new_status = status_change["new"]
        if new_status == Article.Status.PUBLISHED:
            return AuditLog.Action.PUBLISH
        if new_status == Article.Status.ARCHIVED:
            return AuditLog.Action.ARCHIVE
        return AuditLog.Action.UPDATE

    deleted_change = changes.get("is_deleted")
    if deleted_change and deleted_change["new"] is True:
        return AuditLog.Action.DELETE

    return AuditLog.Action.UPDATE

@receiver(post_save, sender=Article)
def log_article_save(sender, instance, created, **kwargs):
    if created:
        changes = _diff(None, instance)
        action = AuditLog.Action.CREATE
    else:
        old = getattr(instance, "_old_state", None)
        changes = _diff(old, instance)
        if not changes:
            return
        action = _resolve_action(changes)

    AuditLog.objects.create(
        article=instance,
        user=get_current_user(),
        action=action,
        changes=changes
    )

@receiver(pre_delete, sender=Article)
def log_article_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        article=None,
        user=get_current_user(),
        action=AuditLog.Action.DELETE,
        changes={field: {"old": getattr(instance, field), "new": None} for field in TRACKED_FIELDS},
    )
