from django.forms import ModelForm
from .models import Photo

from django import forms

from . import models


from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm
)
from django.contrib.auth import get_user_model




class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProfileEditForm(ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 全てのフィールドを必須にする
        for k in self.fields:
            self.fields[k].required = True

    class Meta:
        model = models.UserInfoEdit
        fields = (
            'username',
            'icon',
            'introduction'
        )
        

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'comment', 'image', 'category']
        
