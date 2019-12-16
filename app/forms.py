from django.forms import ModelForm
from .models import Photo

from django import forms

from . import models


class ProfileEditForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 全てのフィールドを必須にする
        for k in self.fields:
            self.fields[k].required = True

    class Meta:
        model = models.User
        fields = (
            'username',
            'password',
        )
        

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'comment', 'image', 'category']
        
