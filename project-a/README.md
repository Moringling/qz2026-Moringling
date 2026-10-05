# 文章管理系统

## 总览

本项目是 https://git.itouc.cn/ITStudio_OUC/ProgrammeHomework/src/branch/main/project-a 的实现。

本项目实现一个基本的文章管理系统。用户可在注册登录后，发表文章，向文章添加附件。文章支持草稿、发布、归档三种状态。删除文章时，文章被标记为已删除且不可见，但数据库中仍保留。

本项目实现了 Django 信号驱动的审计日志。

## 功能需求

1. 数据模型：`Article`, `Attachment`, `AuditLog`
2. 附件管理
3. 操作审计：Django 新号驱动
4. 浏览量计数：并发安全
5. 封面图缩略图：上传附件会自动生成200px宽的缩略图。相关代码见 `articles/utils.py`
6. 文章统计视图：`/stats/`
7. 软删除：删除文章标记 `is_deleted=True`，文章保留在数据库中，审计日志保留。已删除的文章在网页上不可见。
8. 附件下载计数：并发安全。


## 运行

### 依赖安装

```shell
pip install -r requirements.txt
```

### 数据库迁移

```shell
python manage.py makemigrations
python manage.py migrate
```

### 运行方式

```shell
python manage.py runserver
```