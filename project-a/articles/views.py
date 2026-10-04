import os.path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Model, F
from django.db.models.aggregates import Count, Sum
from django.db.models.functions import Coalesce
from django.http.request import HttpRequest
from django.http.response import HttpResponse, Http404, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import ArticleForm, AttachmentForm, RegisterForm
from .models import Article, Attachment, AuditLog
from .utils import generate_thumbnail

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "注册成功，请登录。")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

def article_list(request: HttpRequest) -> HttpResponse:
    articles = (
        Article.objects.filter(is_deleted=False)
        .select_related("author")
        .annotate(attachment_count=Count("attachments"))
    )
    return render(request, "articles/article_list.html", {"articles": articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, is_deleted=False)
    Article.objects.filter(pk=pk).update(views=F("views") + 1)
    article.refresh_from_db(fields=["views"])

    audit_logs = (
        article.audit_logs.select_related("user")
        .only("id", "action", "changes", "timestamp", "user__username")[:50]
    )
    attachments = article.attachments.all()
    attachment_form = AttachmentForm()
    is_author = request.user.is_authenticated and request.user == article.author

    return render(
        request,
        "articles/article_detail.html",
        {
            "article": article,
            "audit_logs": audit_logs,
            "attachments": attachments,
            "attachment_form": attachment_form,
            "is_author": is_author,
        }
    )

@login_required
def article_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "创建成功！")
            return redirect(article.get_url())
    else:
        form = ArticleForm()
    return render(request, "articles/article_form.html", {"form": form, "title": "新建文章"})

@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk, is_deleted=False)
    if article.author != request.user:
        messages.error(request, "只能修改自己的文章")
        return redirect(article.get_url())
    if request.method == "POST":
        form = ArticleForm(request.POST,instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "成功更新文章")
            return redirect(article.get_url())
    else:
        form = ArticleForm(instance=article)
    return render(
        request,
        "articles/article_form.html",
        {"form":form, "title": "编辑文章", "article": article }
    )

@login_required
@require_POST
def article_publish(request, pk):
    article = get_object_or_404(Article, pk=pk, is_deleted=False)
    if article.author != request.user:
        messages.error(request, "您不是该文章的作者")
    else:
        article.status = Article.Status.PUBLISHED
        article.save(update_fields=["status", "updated_at"])
        messages.success(request, "成功发布文章")
    return redirect(article.get_url())

@login_required
@require_POST
def article_archive(request, pk):
    article = get_object_or_404(Article, pk=pk, is_deleted=False)
    if article.author != request.user:
        messages.error(request, "您不是该文章的作者")
    else:
        article.status = Article.Status.ARCHIVED
        article.save(update_fields=["status", "updated_at"])
        messages.success(request, "成功归档文章")
    return redirect(article.get_url())

@login_required
@require_POST
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk, is_deleted=False)
    if article.author != request.user:
        messages.error(request, "您不是该文章的作者")
        return redirect(article.get_url())
    article.is_deleted = True
    article.save(update_fields=["is_deleted", "updated_at"])
    messages.success(request, "成功删除文章")
    return redirect("articles:list")

@login_required
def attachment_upload(request, pk):
    article = get_object_or_404(Article, pk=pk, is_deleted=False)
    if article.author != request.user:
        messages.error(request, "您不是该文章的作者")
        return redirect(article.get_url())
    if request.method == "POST":
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.article = article
            attachment.filename = os.path.basename(attachment.file.name)
            attachment.save()

            generate_thumbnail(attachment)
            messages.success(request, "附件上传成功")
            return redirect(article.get_url())
    else:
        form = AttachmentForm()
    return render(request, "articles/attachment_form.html", {"form": form, "article": article})

@login_required
@require_POST
def attachment_delete(request, pk):
    attachment = get_object_or_404(Attachment, pk=pk, article__is_deleted=False)
    if attachment.article.author != request.user:
        messages.error(request, "您不是该文章的作者，无法删除此附件")
        return redirect(attachment.article.get_url())

    article = attachment.article
    if attachment.file:
        attachment.file.delete(save=False)
    if attachment.thumbnail:
        attachment.thumbnail.delete(save=False)
    attachment.delete()
    messages.success(request, "附件已删除")
    return redirect(article.get_url())

def attachment_download(request, pk):
    attachment = get_object_or_404(Attachment, pk=pk, article__is_deleted=False)
    Attachment.objects.filter(pk=pk).update(downloads=F("downloads") + 1)

    try:
        file_handle = attachment.file.open("rb")
    except (FileNotFoundError, ValueError):
        raise Http404("附件不存在")

    return FileResponse(
        file_handle,
        as_attachment=True,
        filename = (attachment.filename) or str(os.path.basename(attachment.file.name))
    )


def stats(request):
    articles = Article.objects.filter(is_deleted=False)
    totals = articles.aggregate(
        total_articles = Count("id"),
        total_views = Coalesce(Sum("views"), 0)
    )
    counts = dict(articles.values_list("status").annotate(count=Count("id")))
    status_counts = [
        {"status": status, "label": label, "count": counts.get(status, 0) }
        for status, label in Article.Status.choices
    ]
    context = {
        **totals,
        "status_counts": status_counts,
        "recent_logs": (
            AuditLog.objects.select_related("article", "user").order_by("-timestamp")[:10]
        )
    }
    return render(request, "articles/stats.html", context)
