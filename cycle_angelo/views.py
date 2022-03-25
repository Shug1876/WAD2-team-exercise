from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views import View
from cycle_angelo.forms import PostForm, CommentForm, UserForm, UserProfileForm
from cycle_angelo.models import Comment, Post, UserProfile


def index(request):
    context_dict = {}

    # Get top 5 posts
    top_post_list = Post.objects.order_by('-number_of_comments')[:5]
    new_post_list = Post.objects.order_by('-created_on')

    # Get visits
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    context_dict['new_posts'] = new_post_list
    context_dict['top_posts'] = top_post_list

    return render(request, 'cycle_angelo/index.html', context=context_dict)

def contact_us(request):
    context_dict = {}

    return render(request, 'cycle_angelo/contact_us.html', context=context_dict)


@login_required
def add_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid:

            post = form.save(commit=False)
            post.creator = request.user
            post.save()

            return redirect('/cycle_angelo/')
        else:
            print(form.errors)

    return render(request, 'cycle_angelo/add_post.html', {'form': form})

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

    try:
        post = Post.objects.get(slug=post_name_slug)
    except Post.DoesNotExist:
        post = None

    if (post == None):
        return redirect('/cycle_angelo/')

    form = CommentForm()
    context_dict['form'] = form
    if request.method == 'POST':
        form = CommentForm(request.POST)


        if form.is_valid:
            if post:
                post.number_of_comments += 1
                post.save()
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()

                return render(request,'cycle_angelo/post.html', context=context_dict)
        else:
            print(form.errors)
    

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
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'cycle_angelo/register.html/',
                  context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


@login_required
def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()

            return redirect(reverse('cycle_angelo:index'))

        else:
            print(form.errors)

    context_dict = {'form': form}

    return render(request, 'cycle_angelo/profile_registration.html', context_dict)


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


class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture})
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('cycle_angelo:index'))

        post_list = Post.objects.all()

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form,
                        'posts': post_list}

        return render(request, 'cycle_angelo/profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('cycle_angelo:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}

        return render(request, 'cycle_angelo/profile.html', context_dict)


# Cookie helpers

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val

    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
        request.session['visits'] = visits
