from django import forms

from .models import Article, Attachment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "body", "status"]
        widgets = {
            "title": forms.TextInput(),
            "body": forms.Textarea(attrs={"rows": 10}),
            "status": forms.Select(),
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ["file"]
        widgets = {"file": forms.ClearableFileInput()}

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        if uploaded and len(uploaded.name) > 255:
            raise forms.ValidationError("文件名过长（最多 255 个字符）")
        return uploaded
