from django import forms
from .models import ForumUser, ForumPost, ForumComment


class ForumLoginForm(forms.Form):
    """
    Form untuk login forum dengan email/username dan password
    """
    identifier = forms.CharField(
        label='Email atau Username',
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-12 pr-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-offset-0',
            'placeholder': 'Email atau username Anda',
            'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-12 pr-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-offset-0',
            'placeholder': 'Masukkan password Anda',
            'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
        })
    )


class ForumRegisterForm(forms.Form):
    """
    Form untuk registrasi forum user baru
    """
    username = forms.CharField(
        max_length=100,
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-12 pr-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-offset-0',
            'placeholder': 'Masukkan username Anda',
            'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full pl-12 pr-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-offset-0',
            'placeholder': 'nama@email.com',
            'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
        })
    )
    role = forms.ChoiceField(
        choices=ForumUser.ROLE_CHOICES,
        label='Kategori',
        widget=forms.Select(attrs={
            'class': 'w-full pl-12 pr-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-offset-0 appearance-none bg-white cursor-pointer',
            'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
        })
    )
    password = forms.CharField(
        label='Password',
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-12 pr-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-offset-0',
            'placeholder': 'Minimal 6 karakter',
            'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
        }),
        help_text='Password minimal 6 karakter'
    )
    confirm_password = forms.CharField(
        label='Konfirmasi Password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-12 pr-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-offset-0',
            'placeholder': 'Ulangi password Anda',
            'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password tidak cocok.')
        
        return cleaned_data


class ForumPostForm(forms.ModelForm):
    """
    Form untuk membuat dan mengedit postingan forum
    """
    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-offset-0',
                'placeholder': 'Masukkan judul postingan',
                'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base resize-none focus:outline-none focus:ring-2 focus:ring-offset-0',
                'rows': 10,
                'placeholder': 'Tulis isi postingan Anda di sini...',
                'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base focus:outline-none focus:ring-2 focus:ring-offset-0 appearance-none bg-white cursor-pointer',
                'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
            })
        }
        labels = {
            'title': 'Judul Postingan',
            'content': 'Isi Postingan',
            'category': 'Kategori',
        }


class ForumCommentForm(forms.ModelForm):
    """
    Form untuk menambah komentar
    """
    class Meta:
        model = ForumComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3.5 rounded-xl border transition-all duration-300 font-light text-sm sm:text-base resize-none focus:outline-none focus:ring-2 focus:ring-offset-0',
                'rows': 4,
                'placeholder': 'Tulis komentar Anda di sini...',
                'style': 'border-color: rgba(229, 231, 235, 0.6); background: rgba(255, 255, 255, 0.8);'
            })
        }
        labels = {
            'content': 'Komentar',
        }

