import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2_team_exercise.settings')

import django

django.setup()

from cycle_angelo.models import User, Post, Comment
import random


def populate():
    post1_comments = ['Nice ride!', 'Wow that was fast!']
    post2_comments = ['How much did that cost?!', 'Ready to race you soon!']
    post3_comments = ['If you add intervals to training that might help',
                      'Make sure to sleep enough']

    test_blogPosts = {'What a day to go out in the bike! 80k\'s in the bank.': {'comments': post1_comments},
                      'New bike day, ready for some miles in the summer!': {'comments': post2_comments},
                      'Wanting to stay motivated and get better on the bike. Any ideas?': {'comments': post3_comments}}

    for blogPost, comments in test_blogPosts.items():
        bp = add_post(blogPost)
        for c in comments['comments']:
            add_comment(bp, c)

def add_post(bp):
    creator = User(username="username" + str(random.randint(1, 1000)))
    creator.save()
    content = bp
    bp = Post.objects.get_or_create(creator=creator, content=content)[0]
    bp.save()
    return bp


def add_comment(bp, content):
    user = User(username="username" + str(random.randint(1, 1000)))
    user.save()
    c = Comment.objects.get_or_create(post=bp, user=user, content=content)[0]
    bp.number_of_comments = bp.number_of_comments + 1
    bp.save()
    c.save()
    return c


if __name__ == '__main__':
    print('Starting Cycle Angelo population script...')
    populate()
