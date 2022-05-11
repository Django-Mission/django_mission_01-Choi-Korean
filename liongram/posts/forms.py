from dataclasses import field
from unicodedata import category
from django import forms
from .models import Post
from django.core.exceptions import ValidationError


# 현재 수준에서는 Form과 모델이랑 비슷하다고 보면 됨
# class PostBaseForm(forms.Form): # forms.Form 상속 받기
#     CATEGORY_CHOICES = [
#         ('1', '일반'),
#         ('2', '계정'),
#     ]
#     image = forms.ImageField(label="이미지")    # label = verbose_name과 마찬가지로 필드소개 이름 설정
#     content = forms.CharField(label="내용", widget=forms.Textarea, required=True)   # required : 필수 field 설정
#     category = forms.ChoiceField(label="카테고리", choices=CATEGORY_CHOICES)

class PostBaseForm(forms.ModelForm):  # model은 Post인 field는 전체항목인 form 생성하는 class. 와 개쩐당
    class Meta:
        model = Post
        fields = '__all__'

class PostCreateForm(PostBaseForm): # 객체지향이래 이게. interface식으로 상속받아서 하는거 보여주는 건가?
    class Meta(PostBaseForm.Meta):
        fields = ['image', 'content']
    def clean_content(self):    # clean_  + content(필드명) 하면 해당 필드명(content)에 대한 유효성 검사 함수가 되게됨. django의 약속임
        data = self.cleaned_data['content']
        if "비속어" == data:
            raise ValidationError("비속어는 사용하실 수 없습니다.")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

# 이렇게 update, detail form 다 만들 수 있대.


class PostDetailForm(PostBaseForm):
    def __init__(self, *args, **kwargs):
        super(PostDetailForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['disabled'] = True
    pass