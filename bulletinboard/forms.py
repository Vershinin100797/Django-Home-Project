from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Profile, Comment


class AnnouncementPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['announcement_title', 'description', 'category', 'announcement_image', 'price']
        labels = {
            'announcement_title': 'Заголовок объявления',
            'description': 'Описание объявления',
            'category': 'Выберите категорию',
            'announcement_image': 'Выберите файл',
            'price': 'Укажите цену'
        }
        widgets = {
            'announcement_title': forms.TextInput(attrs={'class': 'create-form-input', 'placeholder': 'Введите заголовок объявления'}),
            'description': forms.Textarea(attrs={'class': 'create-form-textarea', 'placeholder': 'Описание объявления'}),
            'category': forms.Select(attrs={'class': 'create-form-input'}),
            'announcement_image': forms.FileInput(attrs={'type': "file", 'class': "custom-file-upload"}),
            'price': forms.NumberInput(attrs={'class': 'create-form-input', 'placeholder': 'Ведите цену'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'announcement-comment-form-control', 'placeholder': 'Оставить отзыв'})
        }


from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):

     username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Логин',
                                                            'class': 'login-form-input'}))

     password = forms.CharField(
         label="Пароль",
         strip=False,
         widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'login-form-input'}),
     )

     error_messages = {
         'invalid_login': "Введен неправильный логин или пароль",
     }


class SignupForm(UserCreationForm):
     error_messages = {
         'password_mismatch': "Пароли не совпадают.",
     }

     password1 = forms.CharField(
         label="Пароль",
         strip=False,
         widget=forms.PasswordInput(attrs={'class': 'signup-form-input', 'placeholder': 'Пароль'})
     )

     password2 = forms.CharField(
         label="Подтверждение пароля",
         widget=forms.PasswordInput(attrs={'class': 'signup-form-input', 'placeholder': 'Подтвердите пароль'}),
         strip=False,
         help_text="Введите тот же пароль, что и выше",
     )

     class Meta:
         model = User
         fields = ('email', 'username')
         widgets = {
             'username': forms.TextInput(attrs={'class': 'signup-form-input', 'placeholder': 'Логин'}),
             'email': forms.EmailInput(attrs={'autofocus': True, 'class': 'signup-form-input', 'placeholder': 'Email'}),
         }

     def clean_email(self):
         email = self.cleaned_data.get('email')
         username = self.cleaned_data.get('username')
         if email and User.objects.filter(email=email).exclude(username=username).exists():
             raise forms.ValidationError('Email addresses must be unique.')
         return email


class UpdateProfileForm(forms.ModelForm):
    birth_date = forms.DateField(label="Дата рождения", input_formats=['%d-%m-%Y'],
                                 widget=forms.DateInput(format=('%d-%m-%Y'), attrs={'class': 'create-form-input',
                                                              'placeholder': 'Дата рождения в формате dd-mm-yyyy'}))

    class Meta:
        model = Profile
        fields = ['birth_date', 'user', 'avatar']
        labels = {
                'user': "Имя профиля",
                'avatar': "Аватар",
                }
        widgets = {
            'user': forms.TextInput(attrs={'class': 'create-form-input', 'placeholder': 'Имя'}),
            'avatar': forms.FileInput(attrs={'type': "file", 'class': "custom-file-upload"}),
        }
