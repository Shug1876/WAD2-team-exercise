from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from cycle_angelo.forms import PostForm, CommentForm, UserForm, UserProfileForm
from cycle_angelo.models import Comment, Post, UserProfile


def index(request):

    context_dict = {}

    post_list = Post.objects.all()

    context_dict['posts'] = post_list

    return render(request, 'cycle_angelo/index.html', context=context_dict)

@login_required
def add_post(request):

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)


        if form.is_valid:

            form.save(commit=True)

            return redirect('/cycle_angelo/')
        else:
            print(form.errors)

    return render(request, 'cycle_angelo/add_post.html', {'form': form})

@login_required
def add_comment(request, post_name_slug):

    try:
        post = Post.objects.get(slug=post_name_slug)
    except Post.DoesNotExist:
        post = None

    if(post == None):
        return redirect('/cycle_angelo/')
    
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid:
            if post:
                comment = form.save(commit=False)
                comment.post = post
                comment.save()

                return redirect(reverse('cycle_angelo:show_post', kwargs={'post_name_slug':post_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form':form, 'post':post}
    return render(request, 'cycle_angelo/add_comment.html', context=context_dict)



def show_post(request, post_name_slug):

    context_dict = {}

    try:
        post = Post.objects.get(slug=post_name_slug)

        comments = Comment.objects.filter(post=post)
        context_dict['comments'] = comments
        context_dict['post'] = post

    except Post.DoesNotExist:

        context_dict['comments'] = None
        context_dict['post'] = None

    return render(request, 'cycle_angelo/post.html', context=context_dict)


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = FILES['picture']

            profile.save()

            registered = True 

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'cycle_angelo/register.html/', 
                  context = {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

def user_login(request):

    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:

                login(request, user)
                return redirect(reverse('cycle_angelo:index'))
            else:
                return HttpResponse("Your Cycle Angelo account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'cycle_angelo/login.html')


def user_logout(request):

    logout(request)

    return redirect(reverse('cycle_angelo:index'))









