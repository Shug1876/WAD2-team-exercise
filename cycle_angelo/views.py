from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from cycle_angelo.forms import PostForm, CommentForm
from cycle_angelo.models import Comment, Post


def index(request):

    context_dict = {}

    post_list = Post.objects.all()

    context_dict['posts'] = post_list

    return render(request, 'cycle_angelo/index.html', context=context_dict)

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







