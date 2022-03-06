from django import forms
from cycle_angelo.models import Post, Comment, UserProfile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
     content = forms.CharField(max_length=200, help_text='Please enter the text for the post you want to share!')
     slug = forms.CharField(widget=forms.HiddenInput(), required=False)
     
     class Meta:
         model = Post
         fields = ('content',)
    
class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=150)
    
    class Meta:
        model = Comment
        exclude = ('post',)
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
