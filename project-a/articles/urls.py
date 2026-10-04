from django.urls import path

from . import views

app_name = "articles"

urlpatterns = [
    path("", views.article_list, name="list"),
    path("stats/", views.stats, name="stats"),
    path("articles/new/", views.article_create, name="create"),
    path("articles/<int:pk>/", views.article_detail, name="detail"),
    path("articles/<int:pk>/edit/", views.article_update, name="update"),
    path("articles/<int:pk>/publish/", views.article_publish, name="publish"),
    path("articles/<int:pk>/archive/", views.article_archive, name="archive"),
    path("articles/<int:pk>/delete/", views.article_delete, name="delete"),
    path("articles/<int:pk>/attachments/upload/", views.attachment_upload, name="attachment_upload"),
    path("attachments/<int:pk>/delete/", views.attachment_delete, name="attachment_delete"),
    path("attachments/<int:pk>/download/", views.attachment_download, name="attachment_download"),
]
