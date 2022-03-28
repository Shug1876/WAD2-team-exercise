from django import forms
from cycle_angelo.models import Post, Comment, UserProfile
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    title = forms.CharField(help_text="Want to add a title? Add one here!", required=False)
    content = forms.CharField(max_length=1000, help_text='Please enter the text for the post you want to share!')
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
     
    class Meta:
        model = Post
        fields = ('title','content',)
    
class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=300)
    
    class Meta:
        model = Comment
        exclude = ('post','user',)
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)
