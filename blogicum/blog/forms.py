from django import forms

from .models import User, Post, Comment


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False, label='Имя')
    last_name = forms.CharField(
        max_length=150, required=False, label='Фамилия')
    username = forms.CharField(max_length=150, label='Логин')
    email = forms.EmailField(required=False, label='Электронная почта')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',
                  'location', 'category', 'image', 'pub_date',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
