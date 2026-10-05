from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Article, Attachment

class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名", max_length=150, widget=forms.TextInput()
    )
    password1 = forms.CharField(
        label="密码", min_length=8, widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="确认密码", min_length=8, widget=forms.PasswordInput()
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已被占用")
        return username

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "两次输入的密码不一致")
        elif password1:
            try:
                validate_password(password1)
            except ValidationError as ex:
                self.add_error("password1", ex)
        return cleaned

    def save(self):
        user = get_user_model()(username=self.cleaned_data["username"])
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user

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
